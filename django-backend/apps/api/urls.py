from django.urls import path
from . import views

urlpatterns = [
    path('schemas/', views.SchemaListCreateView.as_view(), name='schema-list-create'),
    path('schemas/<int:pk>/', views.SchemaDetailView.as_view(), name='schema-detail'),
    path('chats/', views.ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
]