from urllib.parse import urljoin
import requests
from django.urls import reverse
from rest_framework import generics
from pcshop import settings
from product.models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ResendEmailVerificationView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            email_address = EmailAddress.objects.get(user=request.user, verified=False)
            send_email_confirmation(request, request.user)
            return Response({'detail': 'Verification email has been sent.'}, status=status.HTTP_200_OK)
        except EmailAddress.DoesNotExist:
            return Response(
                {'error': 'No unverified email found for this user.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client
class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        If you are building a fullstack application (eq. with React app next to Django)
        you can place this endpoint in your frontend application to receive
        the JWT tokens there - and store them in the state
        """

        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Remember to replace the localhost:8000 with the actual domain name before deployment
        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(response.json(), status=status.HTTP_200_OK)