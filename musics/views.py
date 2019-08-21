from musics.models import Music
from musics.serializers import MusicSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
# jwt
from rest_framework_simplejwt import authentication

# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    #permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    #parser_classes = (JSONParser,)

    # /api/music/{pk}/song_detail/
    @action(detail=True, methods=['get'])
    def song_detail(self, request, pk=None):
        music = get_object_or_404(Music, pk=pk)
        result = {
            'singer': music.singer,
            'song': music.song
        }

        return Response(result, status=status.HTTP_200_OK)

    # /api/music/all_singer/
    @action(detail=True, methods=['get'])
    def all_singer(self, request):
        music = Music.objects.values_list('singer', flat=True).distinct()
        return Response(music, status=status.HTTP_200_OK)