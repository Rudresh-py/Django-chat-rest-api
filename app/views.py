from rest_framework import generics
from .models import Room, Message
from .serializers import RegisterSerializer, RoomCreateSerializer, RoomSerializer, MessageSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer


class RoomListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    

class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'slug'

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        room = Room.objects.get(slug=room_slug)
        return Message.objects.filter(room=room)
