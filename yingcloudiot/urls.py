"""django_rest_swagger_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

# swagger
from rest_framework_swagger.views import get_swagger_view
# simple-jwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_swagger_view(title='API')

urlpatterns = [
    # django admin app
    path('admin/', admin.site.urls),  
    # swagger API文档
    path('docs/', schema_view),
    # rest
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # jwt
    path('token-api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # rest auth 
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    # my own app
    path('music/', include('musics.urls')), 
    path('accounts/', include('accounts.urls')),
    path('detection/', include('detection.urls')),
]