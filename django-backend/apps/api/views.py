from rest_framework import generics
from .models import Schema, Chat
from .serializers import SchemaSerializer, ChatSerializer

class SchemaListCreateView(generics.ListCreateAPIView):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer

class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class SchemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer

class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer