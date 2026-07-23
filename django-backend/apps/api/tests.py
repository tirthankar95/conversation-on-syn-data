from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Schema, Chat

class SchemaAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.schema_data = {'name': 'Test Schema'}

    def test_create_schema(self):
        response = self.client.post('/api/schemas/', self.schema_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schema.objects.count(), 1)
        self.assertEqual(Schema.objects.get().name, 'Test Schema')

    def test_list_schemas(self):
        Schema.objects.create(name='Test Schema 1')
        Schema.objects.create(name='Test Schema 2')
        response = self.client.get('/api/schemas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ChatAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.chat_data = {'title': 'Test Chat', 'schema_id': 1}

    def test_create_chat(self):
        response = self.client.post('/api/chats/', self.chat_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Chat.objects.get().title, 'Test Chat')

    def test_list_chats(self):
        Chat.objects.create(title='Test Chat 1', schema_id=1)
        Chat.objects.create(title='Test Chat 2', schema_id=1)
        response = self.client.get('/api/chats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)