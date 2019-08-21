# -*- coding: utf-8 -*-
"""
    @Time    : 2019/8/18 20:00
    @Author  : ZhuSheng
    @Email   : 1537017271@qq.com
    @File    : serializers.py
    @Software: PyCharm
"""
from rest_framework import serializers
from detection.models import Picture, Recognition

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'

class RecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recognition
        fields = '__all__'