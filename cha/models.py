# models.py
from django.db import models

class ChatMessage(models.Model):
    user_message = models.TextField()
    system_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user_message[:50]} - System: {self.system_response[:50]}"
