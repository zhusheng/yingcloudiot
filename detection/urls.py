# -*- coding: utf-8 -*-
"""
    @Time    : 2019/8/18 20:01
    @Author  : ZhuSheng
    @Email   : 1537017271@qq.com
    @File    : urls.py
    @Software: PyCharm
"""
from django.conf.urls import url, include
from django.urls import path
# rest router
from rest_framework.routers import DefaultRouter
from detection.views import PictureViewSet, RecognitionViewSet

router = DefaultRouter()
router.register('picture', PictureViewSet, base_name='picture')
router.register('recognition', RecognitionViewSet, base_name='recognition')

urlpatterns = [
    path('', include(router.urls)),
]
