from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()


class ProductDescriptionRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)


class ProductDescriptionResponseSerializer(serializers.Serializer):
    description = serializers.CharField()
    keywords = serializers.ListField(child=serializers.CharField())


class ImageRecognitionSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageRecognitionResponseSerializer(serializers.Serializer):
    keywords = serializers.ListField(child=serializers.CharField())
