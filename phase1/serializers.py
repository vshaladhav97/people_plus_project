import os
from django.db.models import Q
# from apps.portal_app.models import *
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
# from .utils import Google,Facebook,Twitter,register_social_user
User = get_user_model()
# #Serializer to Get User Details using Django Token Authentication
# class UserSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = User
#     fields = ["id", "first_name", "last_name", "username", "email"]
#
#
# #Serializer to Register User
# class RegisterSerializer(serializers.ModelSerializer):
#
#   email = serializers.EmailField(
#     required=True,
#     validators=[UniqueValidator(queryset=User.objects.all())]
#   )
#   password = serializers.CharField(
#     write_only=True, required=True, validators=[validate_password])
#   password2 = serializers.CharField(write_only=True, required=True)
#   class Meta:
#     model = User
#     fields = ('username', 'password', 'password2',
#          'email', 'first_name', 'last_name')
#     extra_kwargs = {
#       'first_name': {'required': True},
#       'last_name': {'required': True},
#       'username': {'required': True},
#     }
#   def validate(self, attrs):
#     if attrs['password'] != attrs['password2']:
#       raise serializers.ValidationError(
#         {"password": "Password fields didn't match."})
#     return attrs
#   def create(self, validated_data):
#     user = User.objects.create(
#       username=validated_data['username'],
#       email=validated_data['email'],
#       first_name=validated_data['first_name'],
#       last_name=validated_data['last_name']
#     )
#     user.set_password(validated_data['password'])
#     user.save()
#     return user


# Registration  Serializer
class RegistrationSerializer(serializers.ModelSerializer):
    email    = serializers.EmailField()
    username = serializers.CharField(max_length=150, min_length=3)
    password = serializers.CharField(max_length=150, write_only=True)

    def validate(self, args):
        email    = args.get('email', None)
        username = args.get('username', None)
        password = args.get('password', '')
        if email is None or email == "":
            raise serializers.ValidationError({'error': ('Email is required.')})
        elif username is None or username == "":
            raise serializers.ValidationError({'error': ('Username is required.')})
        elif User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'error': ('username already exists.')})
        elif User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'error': ('email already exists.')})
        elif (len(password) < 5 and len(password) <= 15):
            raise serializers.ValidationError({'error': ('Ensure password has at least 5 characters and maximum 15 characters.')})
        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

# Login Serializer
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, min_length=3)
    password = serializers.CharField(max_length=150, write_only=True)
    tokens   = serializers.CharField(max_length=150, read_only=True)

    class Meta:
        model  = User
        fields = ['username','password','tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if username and password:
            try:
                user = User.objects.get(Q(username=username)|Q(email=username))
                if user is None:
                    return {'msg':'Incorrect Username','is_verified':False}
                # if not user.is_active:
                #     return {'msg': 'Account disabled, contact admin', 'is_verified':user.is_verified}

                if User.objects.filter(Q(username=user.username)|Q(email=user.email)).exists():
                    password_valid = user.check_password(password)
                    if password_valid:
                        return {'username': user.username,'tokens':user.tokens}
                    else:
                        return {'msg':'Incorrect Password','is_verified': user.is_verified}
            except:
                return {'msg':'Invalid credentials, try again','is_verified': False}
        else:
            return {'msg': 'Invalid credentials, try again','is_verified': False}


class UserFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "dob", "gender", "profile_image", "created_date", "modified_date",]

