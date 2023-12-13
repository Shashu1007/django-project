import spacy
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, ImageRecognitionResponseSerializer, ImageRecognitionSerializer
from .serializers import ProductDescriptionRequestSerializer, ProductDescriptionResponseSerializer
from .serializers import RegisterSerializer
import cv2 as cv


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, generate or retrieve a token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key})
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class ProductDescriptionView(generics.CreateAPIView):
    serializer_class = ProductDescriptionRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data['title']

        # Generate product description (replace this with your actual logic)
        description = generate_product_description(title)

        # Extract keywords from the generated description
        keywords = extract_keywords(description)

        response_data = {'description': description, 'keywords': keywords}
        response_serializer = ProductDescriptionResponseSerializer(response_data)
        return Response(response_serializer.data)


def generate_product_description(title):
    # Replace this with your actual logic to generate a product description
    return f"This is a product description for {title}. It is a wonderful product that you should consider."


def extract_keywords(description):
    # Replace this with your actual logic to extract keywords
    # For simplicity, using a dummy list
    return ['keyword1', 'keyword2', 'keyword3']


# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")


class ImageRecognitionView(generics.CreateAPIView):
    serializer_class = ImageRecognitionSerializer

    def create(self, request, *args, **kwargs):
        # Validate request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract image from validated data
        image = serializer.validated_data['image']

        # Perform image recognition (replace this logic with your actual image recognition logic)
        keywords = recognize_image(image)

        # Prepare the response data
        response_data = {'keywords': keywords}

        # Serialize and return the response
        response_serializer = ImageRecognitionResponseSerializer(response_data)
        return Response(response_serializer.data)


def recognize_image(image, cv2=cv):
    img = cv.imread(image.path, cv.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv.Canny(img, 50, 150)

    # Extract keywords from the processed image using spaCy
    description = "This is an image description from OpenCV processing."
    doc = nlp(description)

    # Extract keywords
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return keywords




