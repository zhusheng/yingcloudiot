from accounts.models import MyProfile
from rest_framework import serializers
from django.contrib.auth.models import User

class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProfile
        #fields = ('phone_num', 'mugshot')
        fields = '__all__'