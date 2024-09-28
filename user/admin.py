from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, UserDevice

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.password:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomUserAdmin(UserAdmin):
    form = CustomUserCreationForm
    
    list_display = ['first_name', 'last_name', 'phone_number', 'email']  

    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Customize fieldsets to include all fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 'phone_number', 'deposite', 'caunty', 'region', 'avatar', 'company')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'roles')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('OTP Info', {'fields': ('otp_counter', 'otp_sent_time', 'otp_tried', 'otp_attempts')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 'deposite', 'caunty', 'region', 'avatar', 'is_active', 'is_staff', 'is_superuser', 'roles'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(UserDevice)
