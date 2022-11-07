from django.urls import path
from .views import peer1, peer2, peer

urlpatterns = [
    path('video_chat/', peer, name='peer'),
    path('video_chat/peer1/', peer1, name='peer1'),
    path('video_chat/peer2/', peer2, name='peer2'),
]