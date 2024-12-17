# backend/authapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .auth_service import AuthService, User
from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)

class PhoneLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number', '').strip()
        auth_service = AuthService()
        response_data, status_code = auth_service.initiate_phone_login(phone_number)
        return Response(response_data, status=status_code)

class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number', '').strip()
        submitted_otp = request.data.get('otp', '').strip()
        auth_service = AuthService()
        response_data, status_code = auth_service.verify_otp(phone_number, submitted_otp)
        return Response(response_data, status=status_code)

@api_view(['POST'])
def check_phone(request):
    try:
        phone_number = request.data.get('phone_number', '').strip()
        exists = User.objects.filter(phone_number=phone_number).exists()
        return Response({'exists': exists})
    except Exception as e:
        logger.error(f"Error in check phone: {str(e)}")
        return Response({'error': str(e)}, status=500)    