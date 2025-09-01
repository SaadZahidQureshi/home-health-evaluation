from conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from api.core.abstract import BaseModel
from api.core.choices import CharFieldSizes, CustomerTypes, Roles
from api.core.validators import phone_regex


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", Roles.ADMIN)
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
        

class User(AbstractUser, BaseModel):
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=CharFieldSizes.LARGE, null=True)
    role = models.CharField(choices=Roles.choices, max_length=CharFieldSizes.SMALL, default=Roles.USER)
    phone = models.CharField(max_length=20, validators=[phone_regex], null=True, blank=True, unique=True, default=None)
    image = models.ImageField(upload_to="profiles/", default=settings.DEFAULT_PROFILE_IMAGE, null=True, blank=True)
    objects = UserManager()

    def __str__(self):
        return self.email if self.email else self.role
    

class Customer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_user")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_created_by")
    house_image = models.ImageField(upload_to="house_images/", null=True, blank=True)
    address = models.CharField(max_length=CharFieldSizes.LARGE, null=True)
    city = models.CharField(max_length=CharFieldSizes.SMALL, null=True)
    state = models.CharField(max_length=CharFieldSizes.SMALL, null=True)
    zip = models.CharField(max_length=CharFieldSizes.SMALL, null=True)
    audit_completed = models.BooleanField(default=False)
    type = models.CharField(choices=CustomerTypes.choices, max_length=CharFieldSizes.SMALL, default=CustomerTypes.HEALTHY_HOME)

    @classmethod
    def create_default_customer(self, obj):
        from .serializers import ShortUserSerializer
        user_data = {
            "name": None,
            "email": None,
            "role": Roles.CUSTOMER
        }
        user_serializer = ShortUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return self.objects.create(user=user,address=None,city=None,state=None,zip=None, created_by=obj)
    

class Photo(BaseModel):
    image = models.ImageField(upload_to='answer_photos/')

    def __str__(self):
        return f"Photo {self.id}"
