from django.db import models
from django.contrib.auth.models import User
from vehicle.models import Customer, Request

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"Session {self.id}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    is_bot = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    related_request = models.ForeignKey(Request, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['timestamp']