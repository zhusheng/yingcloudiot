from django.conf.urls import url, include
from django.urls import path
from accounts.views import MyProfileViewSet
# rest router
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', MyProfileViewSet, base_name='accounts')

urlpatterns = [
    path('', include(router.urls)),
]

# 参考设置扩展官方的User Model
# https://www.jianshu.com/p/d45a687c3f41