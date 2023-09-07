
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'user', userView)
router.register(r'dealerview', DealerViewSet)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', AuthView.as_view(), name='login'),
    # path('user/<int:id>/', User_data, name='user'),
    path('dealer/', DealerRegistrationView.as_view()),
    path('otp/', OtpView.as_view(), name='otp'),
    path('',include(router.urls)),
    path('token/refresh/', ObtainNewAccessToken.as_view()),

    # Other URL patterns for your application
]
