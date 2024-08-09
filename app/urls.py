from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, RoomCreateView, RoomListView, RoomDetailView, MessageListView, LogoutView

urlpatterns = [
    path('api/rooms/', RoomListView.as_view(), name='room-list'),
    path('api/rooms/create/', RoomCreateView.as_view(), name='room-create'),
    path('api/rooms/<slug:slug>/', RoomDetailView.as_view(), name='room-detail'),
    path('api/rooms/<slug:room_slug>/messages/', MessageListView.as_view(), name='message-list'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
]
