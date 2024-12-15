import random
import re
from django.core.cache import cache
from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def validate_phone_number(phone):
        pattern = r'^0[0-9]{10}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def save_otp(phone_number, otp):
        cache_key = f'otp_{phone_number}'
        cache.set(cache_key, otp, timeout=120)

    @staticmethod
    def get_otp(phone_number):
        cache_key = f'otp_{phone_number}'
        return cache.get(cache_key)

    @staticmethod
    def delete_otp(phone_number):
        cache_key = f'otp_{phone_number}'
        cache.delete(cache_key)

    @staticmethod
    def send_otp(phone_number, otp):
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'receptor': phone_number,
            'template': "otpservice",
            'token': otp,
            'type': 'sms'
        }
        return api.verify_lookup(params)

    def initiate_phone_login(self, phone_number):
        """Handle the phone login process"""
        if not phone_number:
            return {'error': 'Phone number is required'}, 400

        if not self.validate_phone_number(phone_number):
            return {
                'error': 'Invalid phone number format. Must start with 0 followed by 10 digits'
            }, 400

        try:
            otp = self.generate_otp()
            logger.info(f"Generated OTP for {phone_number}: {otp}")
            
            self.save_otp(phone_number, otp)
            self.send_otp(phone_number, otp)

            is_new_user = not User.objects.filter(phone_number=phone_number).exists()
            return {
                'message': 'OTP sent successfully',
                'is_new_user': is_new_user
            }, 200

        except (APIException, HTTPException) as e:
            logger.error(f"Kavenegar error for {phone_number}: {str(e)}")
            return {
                'error': 'Failed to send OTP. Please try again later.'
            }, 503
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'error': 'An unexpected error occurred'
            }, 500

    def verify_otp(self, phone_number, submitted_otp):
        """Handle the OTP verification process"""
        if not phone_number or not submitted_otp:
            return {
                'error': 'Phone number and OTP are required'
            }, 400

        if not self.validate_phone_number(phone_number):
            return {
                'error': 'Invalid phone number format'
            }, 400

        cached_otp = self.get_otp(phone_number)
        logger.info(f"Phone: {phone_number}, Cached OTP: {cached_otp}, Submitted OTP: {submitted_otp}")

        if not cached_otp:
            return {
                'error': 'OTP has expired'
            }, 400

        if str(cached_otp) != str(submitted_otp):
            return {
                'error': 'Invalid OTP'
            }, 400

        try:
            user, created = User.objects.get_or_create(phone_number=phone_number)
            self.delete_otp(phone_number)

            refresh = RefreshToken.for_user(user)
            
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'phone_number': user.phone_number,
                    'is_new_user': created
                }
            }, 200

        except Exception as e:
            logger.error(f"Error in OTP verification: {str(e)}")
            return {
                'error': 'Failed to verify OTP'
            }, 500