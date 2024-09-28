import requests
import os
import logging
from django.core.mail import send_mail
from django.core.cache import cache
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_token():
    token = cache.get('eskiz_token')  
    if token:
        logger.info("Using cached Eskiz token.")
        return token

    login_url = "https://notify.eskiz.uz/api/auth/login"
    login_payload = {
        "email": os.getenv("ESKIZ_USER_EMAIL"),
        'password': os.getenv('ESKIZ_USER_PASSWORD')
    }

    try:
        login_response = requests.post(login_url, json=login_payload)
        login_response.raise_for_status()
        login_data = login_response.json()

        token = login_data.get('data', {}).get('token')
        if token:
            logger.info("Eskiz token retrieved successfully.")
            cache.set('eskiz_token', token, timeout=3600)
        else:
            logger.error("Token not found in the response. Response data: %s", login_data)
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during Eskiz login: {e}")
        return None
    
    return token


def send_sms(recipient, message):
    token=get_token()
    sms_url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    sms_payload = {
        'mobile_phone': recipient,
        'message': message,
        'from': '4546'
    }

    try:
        sms_response = requests.post(sms_url, headers=headers, json=sms_payload)
        sms_response.raise_for_status() 
        sms_data = sms_response.json()

        print("SMS Response JSON:", sms_data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending SMS: {e}")

    print("SMS Response JSON:", sms_response.json())
 

def send_email(recipient, message, subject):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),  
            recipient_list=[recipient],
            fail_silently=False
        )
        logger.info(f"Email sent to {recipient} with subject '{subject}'")
    except Exception as e:
        logger.error(f"An error occurred while sending the email: {e}")