from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    CustomUser, 
    UniqueConfig, 
    Role, 
    UserDevice,
)

from app.models.investor import Investor
from .serializers import UserLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError
import pyotp, re, redis, os, json, uuid, phonenumbers, pytz
from phonenumbers import NumberParseException
from django.utils import timezone
from . import notification
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email
from drf_yasg.utils import swagger_auto_schema

redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', '127.0.0.1'),
    port=int(os.getenv('REDIS_PORT', 6379)),    
    db=int(os.getenv('REDIS_DB', 0))            
)


def validate_password(value):
        if len(value) < 8 or len(value) > 20:
            raise ValidationError(("Password must be between 8 and 20 characters long."))
        
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError(("Password must contain at least one letter."))
        
        if not re.search(r'\d', value):
            raise ValidationError(("Password must contain at least one number."))
        
        return value


class UserTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get('identifier')
        password = request.data.get('password')

        if not identifier or not password:
            return Response({'error': ("User Identifier and password Required")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(identifier)
            is_email = True
        except ValidationError:
            is_email = False

        if is_email:
            try:
                user = CustomUser.objects.get(email=identifier)
            except CustomUser.DoesNotExist:
                return Response({'error': ("User does not exist")}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = CustomUser.objects.get(phone_number=identifier)
            except CustomUser.DoesNotExist:
                return Response({'error': ("User does not exist")}, status=status.HTTP_400_BAD_REQUEST)
        
        if user:
            if not check_password(password, user.password):
                return Response({'error': ('Password did not match')}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        unique_config, created = UniqueConfig.objects.get_or_create(id=1)

        hotp = pyotp.HOTP("somedifficult32string")
        
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        middle_name = request.data.get("middle_name", "")
        birth_date = request.data.get("birth_date")
        gender = request.data.get("gender")
        password = request.data.get("password")
        contact_method = request.data.get("contact_method")
        selected_role = request.data.get("role")

        if not email or not phone_number:
            return Response({"error": "Both email and phone number are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not first_name or not last_name:
            return Response({"error": "First name and last name are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not birth_date:
            return Response({"error": "Birth date is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not gender or gender not in ['male', 'female']:
            return Response({"error": "Valid gender is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if contact_method not in ['email', 'phone']:
            return Response({"error": "Invalid contact method"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not selected_role or selected_role not in {'company', 'investor'}:
            return Response({"error": "Invalid role selected or no role selected"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                return Response({"error": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST)
            phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            return Response({"error": "Invalid phone number format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e: 
            return Response({'error': e.messages}, status=400)

        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(phone_number=phone_number).exists():
            return Response({'error': "User with this email or phone number already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        otp = hotp.at(unique_config.otp_counter + 1)
        unique_config.otp_counter += 1  
        unique_config.save()  

        verification_token = str(uuid.uuid4())

        user_data = {
            "email": email,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "birth_date": birth_date,
            "gender": gender,
            "password": password,
            "otp": otp,
            "otp_counter": unique_config.otp_counter,
            "otp_sent_time": timezone.now().isoformat(),
            "role": selected_role
        }

        redis_client.setex(f"verify_user:{verification_token}", 300, json.dumps(user_data))

        if contact_method == 'phone':
            notification.send_sms(phone_number, f"Investmap.uz tizimidan ro'yxatdan o'tish uchun kod: {otp}")
        else:
            notification.send_email(email, f"Investmap.uz tizimidan ro'yxatdan o'tish uchun kod: {otp}", "Investmap.uz uchun kod verifikatsiya")
        
        return Response(
            {
                "message": f"OTP has been sent to your {contact_method}. Please verify it to complete registration",
                "verification_token": verification_token  
            },
            status=status.HTTP_201_CREATED
        )


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        verification_token = request.data.get("verification_token")
        otp = request.data.get("otp")
        
        if not verification_token or not otp:
            return Response({"error": "Verification token and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data_json = redis_client.get(f"verify_user:{verification_token}")
        if not user_data_json:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data = json.loads(user_data_json)
        
        if user_data['otp'] != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.create(
            email=user_data['email'],
            phone_number=user_data['phone_number'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            middle_name=user_data['middle_name'],
            birth_date=user_data['birth_date'],
            gender=user_data['gender'],
            otp_counter=user_data['otp_counter'],
            otp_sent_time=user_data['otp_sent_time'],
        )
        user.set_password(user_data['password'])
        user.save()

        selected_role = user_data['role']
        role, created = Role.objects.get_or_create(name=selected_role)
        user.roles.set([role])  

        if selected_role == 'investor':
            Investor.objects.create(user=user, investor_type='business_angel')

        redis_client.delete(f"verify_user:{verification_token}")
        
        return Response(
            {"message": "OTP verified successfully. User registration completed."},
            status=status.HTTP_200_OK
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        identifier = request.data.get('identifier')
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0].strip()
        login_method = 'email' if '@' in identifier else 'phone'
        login_attempt_time = timezone.now()

        if serializer.is_valid():
            user = serializer.validated_data['user']

            UserDevice.objects.update_or_create(
                user=user,
                ip_address=ip_address,
                defaults={
                    'login_method': login_method,
                    'can_login': True,
                    'login_attempt_time': login_attempt_time,
                    'last_login': timezone.now()
                }
            )

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            roles = user.roles.values_list('name', flat=True)

            return Response({
                'message': 'Login successful.',
                'refresh': str(refresh),
                'access': str(access_token),
                'roles': list(roles),
            }, status=status.HTTP_200_OK)
        else:
            user = CustomUser.objects.filter(email=identifier).first() if '@' in identifier else CustomUser.objects.filter(phone_number=identifier).first()
            if user:
                UserDevice.objects.create(
                    user=user,
                    ip_address=ip_address,
                    login_method=login_method,
                    can_login=False,
                    login_attempt_time=login_attempt_time,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get("identifier")

        if not identifier:
            return Response({"error": "Phone number or email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        identifier = identifier.strip().lower()

        try:
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(phone_number=identifier)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)

        unique_config = UniqueConfig.objects.first()
        if unique_config:
            otp_counter = unique_config.otp_counter
            UniqueConfig.objects.update(otp_counter=otp_counter + 1)
        else:
            otp_counter = 0 
        
        hotp = pyotp.HOTP("somedifficult32string")
        otp = hotp.at(otp_counter + 1)

        redis_client.setex(f"reset_password_otp:{identifier}", 300, otp) 

        if '@' in identifier:
            notification.send_email(identifier, f"Investmap.uz tizimidagi parolni o'zgartirish uchun kod: {otp}", "Parolni tiklash uchun kod")
        else:
            notification.send_sms(identifier, f"Investmap.uz tizmida parolni tiklash uchun kod: {otp}")

        return Response({"message": f"OTP has been sent to {identifier}"}, status=status.HTTP_200_OK)


class ResetPasswordVerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        otp = request.data.get("otp")

        if not otp:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        identifier = None
        for key in redis_client.keys('reset_password_otp:*'):
            key_str = key.decode('utf-8') 
            stored_otp = redis_client.get(key).decode('utf-8')  
            if stored_otp == otp:
                identifier = key_str.split(":")[1]
                break

        if not identifier:
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        reset_token = str(uuid.uuid4())
        redis_client.setex(f"reset_password_token:{reset_token}", 600, identifier)  

        redis_client.delete(f"reset_password_otp:{identifier}")

        return Response({"reset_token": reset_token}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        reset_token = request.data.get("reset_token")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not reset_token or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        identifier = redis_client.get(f"reset_password_token:{reset_token}")
        if not identifier:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        identifier = identifier.decode()
        print(f"Identifier found: {identifier}")

        try:
            validate_password(new_password)
        except ValidationError as e:
            return Response({'error': e.messages}, status=400)

        try:
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(phone_number=identifier)

            user.set_password(new_password)
            user.save()

            print(f"Password reset successfully for user: {identifier}")

            redis_client.delete(f"reset_password_token:{reset_token}")

            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ForgotPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get("identifier")

        if not identifier:
            return Response({"error": "Phone number or email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        identifier = identifier.strip().lower()

        try:
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(phone_number=identifier)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)

        unique_config = UniqueConfig.objects.first()
        if unique_config:
            otp_counter = unique_config.otp_counter
            UniqueConfig.objects.update(otp_counter=otp_counter + 1)
        else:
            otp_counter = 0 
        
        hotp = pyotp.HOTP("somedifficult32string")
        otp = hotp.at(otp_counter + 1)

        redis_client.setex(f"forgot_password_otp:{identifier}", 300, otp)  

        if '@' in identifier:
            notification.send_email(identifier, f"Investmap.uz tizimidagi parolni tiklash uchun kod: {otp}", "Parolni tiklash uchun kod")
        else:
            notification.send_sms(identifier, f"Investmap.uz tizmida parolni tiklash uchun kod: {otp}")

        return Response({"message": f"OTP has been sent to {identifier}"}, status=status.HTTP_200_OK)
    

class ForgotPasswordVerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        otp = request.data.get("otp")

        if not otp:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        identifier = None
        for key in redis_client.keys('forgot_password_otp:*'):
            key_str = key.decode('utf-8')  
            stored_otp = redis_client.get(key).decode('utf-8')  
            if stored_otp == otp:
                identifier = key_str.split(":")[1]
                break

        if not identifier:
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        reset_token = str(uuid.uuid4())
        redis_client.setex(f"forgot_password_token:{reset_token}", 600, identifier) 

        redis_client.delete(f"forgot_password_otp:{identifier}")

        return Response({"reset_token": reset_token}, status=status.HTTP_200_OK)


class ForgotPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        reset_token = request.data.get("reset_token")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not reset_token or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        identifier = redis_client.get(f"forgot_password_token:{reset_token}")
        if not identifier:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        identifier = identifier.decode()

        try:
            validate_password(new_password)
        except ValidationError as e:
            return Response({'error': e.messages}, status=400)

        try:
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(phone_number=identifier)

            user.set_password(new_password)
            user.save()

            redis_client.delete(f"forgot_password_token:{reset_token}")

            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDevicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_timezone = request.query_params.get('timezone', 'UTC') 
        devices = request.user.devices.all()

        target_timezone = pytz.timezone(user_timezone)

        response_data = []
        for device in devices:
            login_attempt_time_utc = timezone.localtime(device.login_attempt_time, pytz.UTC)
            last_login_utc = timezone.localtime(device.last_login, pytz.UTC) if device.last_login else None

            login_attempt_time_local = login_attempt_time_utc.astimezone(target_timezone)
            last_login_local = last_login_utc.astimezone(target_timezone) if last_login_utc else None

            response_data.append({
                'ip_address': device.ip_address,
                'login_method': device.login_method,
                'can_login': device.can_login,
                'login_attempt_time': login_attempt_time_local,
                'last_login': last_login_local,
            })

        return Response(response_data, status=status.HTTP_200_OK)
 

class RemoveDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        device_id = request.data.get('device_id')

        try:
            device = UserDevice.objects.get(id=device_id, user=request.user)
            device.delete()
            return Response({"message": "Device removed successfully"}, status=status.HTTP_200_OK)
        except UserDevice.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)