import random
import string

from django.db import models

from api.core.abstract import BaseModel


class TokenManagement(BaseModel):
    email = models.EmailField()
    token = models.CharField(max_length=6, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.token}"

    @staticmethod
    def generate_token():
        """Generate random 6 character alphanumeric token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
