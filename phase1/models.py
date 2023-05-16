from django.db import models
from people_connect_plus import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, AbstractUser)
# Create your models here.

# User Detail Table
class User(AbstractUser,PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    username        = models.CharField(max_length=50, unique=True)
    password        = models.CharField(max_length=50, db_index=True)
    email           = models.EmailField(max_length=255, unique=True)
    first_name      = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100, null=True, blank=True)
    dob             = models.DateField(max_length=8,  null=True, blank=True)
    gender          = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image   = models.ImageField(upload_to='user/profile_images/', blank=True, null=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class UserGallary(models.Model):

    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    caption         = models.TextField()
    photos          = models.ImageField(upload_to='user_gallary/images/')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)