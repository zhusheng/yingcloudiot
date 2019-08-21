from django.shortcuts import render
from rest_framework import viewsets
from rest_framework_simplejwt import authentication
from detection.models import Picture, Recognition
from detection.serializers import PictureSerializer, RecognitionSerializer

# Create your views here.
class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    authentication_classes = (authentication.JWTAuthentication,)

class RecognitionViewSet(viewsets.ModelViewSet):
    queryset = Recognition.objects.all()
    serializer_class = RecognitionSerializer
    authentication_classes = (authentication.JWTAuthentication,)