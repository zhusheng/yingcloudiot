from django.conf.urls import url, include
from django.urls import path
# rest router
from rest_framework.routers import DefaultRouter
from musics.views import MusicViewSet

router = DefaultRouter()
router.register('', MusicViewSet, base_name='music')

urlpatterns = [
    path('', include(router.urls)), # 访问music rest api
]