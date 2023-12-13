# myproject/urls.py

from django.urls import path
from myapp.views import CustomObtainAuthToken, LoginView, ProductDescriptionView, ImageRecognitionView

urlpatterns = [
    path('api/login/', CustomObtainAuthToken.as_view(), name='api_login'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/product_description/', ProductDescriptionView.as_view(), name='api_product_description'),
    path('api/image_recognition/', ImageRecognitionView.as_view(), name='api_image_recognition'),
]
