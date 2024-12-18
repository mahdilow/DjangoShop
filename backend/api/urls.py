from django.urls import path, include, re_path
from .views import ProductList, ResendEmailVerificationView
from allauth.account.views import ConfirmEmailView, EmailVerificationSentView

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('', include("dj_rest_auth.urls")),
    
        # Email verification URLs
    path(
        "registration/account-email-verification-sent/",
        EmailVerificationSentView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "registration/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="account_email_verification_resend",
    ),

    path('registration/', include("dj_rest_auth.registration.urls")),
    
]
