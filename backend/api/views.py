from rest_framework import generics
from product.models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


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
