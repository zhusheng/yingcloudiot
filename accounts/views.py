from django.shortcuts import render
from accounts.models import MyProfile
from accounts.serializers import MyProfileSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class  MyProfileViewSet(viewsets.ModelViewSet):
    serializer_class =  MyProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset =  MyProfile.objects.all()