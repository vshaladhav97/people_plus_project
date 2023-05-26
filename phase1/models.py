from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from people_connect_plus import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, AbstractUser)
# Create your models here.

# CustomUser Model
class CustomUser(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,password):
        if not email:
            raise ValueError("Users must have an email address !!")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            first_name = first_name,
            last_name  = last_name,
            email      = email,
            username   = username,
            password   = password,
            is_active  = True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name, last_name,email,username,password):
        user = self.create_user(
            email       =   self.normalize_email(email),
            username    =   username,
            password    =   password,
            first_name  =   '',
            last_name   =   ''
        )
        user.is_superuser = True
        user.is_verified  = True
        user.is_active    = True
        user.is_staff     = True
        user.is_admin     = True
        user.save(using=self._db)
        return user

# User Detail Table
class User(AbstractUser,PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    username        = models.CharField(max_length=50, unique=True)
    password        = models.CharField(max_length=255, db_index=True)
    email           = models.EmailField(max_length=255, unique=True)
    first_name      = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100, null=True, blank=True)
    dob             = models.DateField(max_length=8,  null=True, blank=True)
    gender          = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image   = models.ImageField(upload_to='user/profile_images/', blank=True, null=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    is_verified                 = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=False)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh),'access': str(refresh.access_token)}

    # def save(self):
    #     for field in self._meta.fields:
    #         if field.name == 'profile_image':
    #             field.upload_to = 'user/profile_images/%d' % self.id
    #     super(User, self).save()


class UserGallary(models.Model):

    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    caption         = models.TextField()
    photos          = models.ImageField(upload_to='user_gallary/images/')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.id)

class UserFollowerAndFollowed(models.Model):

    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    followers       = models.ManyToManyField(User, related_name="followers_users")
    followed        = models.ManyToManyField(User,  related_name="followed_users")
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.user.id)