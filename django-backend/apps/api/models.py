from django.db import models

class Schema(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Chat(models.Model):
    schema = models.ForeignKey(Schema, related_name='chats', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat in {self.schema.name} at {self.created_at}"