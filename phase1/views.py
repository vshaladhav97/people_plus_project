import ast

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import *
User = get_user_model()
# Create your views here.

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UserProfileAPIView(generics.GenericAPIView):
    def get(self, request):
        json_data                   = request.data
        user_id                     = json_data['user_id']
        user_data                   = User.objects.get(id = user_id)
        user_dict                   = {}
        user_dict["id"]             = user_data.id
        user_dict["username"]       = user_data.username
        user_dict["email"]          = user_data.email
        user_dict["first_name"]     = user_data.first_name if user_data.first_name else ""
        user_dict["last_name"]      = user_data.last_name if user_data.last_name else ""
        user_dict["dob"]            = user_data.dob
        user_dict["gender"]         = user_data.gender
        user_dict["profile_image"]  = user_data.profile_image.url if user_data.profile_image else ""
        return Response({'result' : user_dict}, status=status.HTTP_200_OK)

# Login API View
class LoginAPIView(generics.GenericAPIView):
   serializer_class = LoginSerializer
   def post(self, request):
       serializer       = LoginSerializer(data=request.data)
       first_time_login = False
       if serializer.is_valid():
           if 'msg' and 'is_verified' in serializer.validated_data:
               return Response(serializer.validated_data,status=status.HTTP_400_BAD_REQUEST)
           else:
               if request.data:
                   if 'username' in request.data:
                       id = User.objects.filter(Q(username=request.data['username'])|Q(email=request.data['username']))
                       if id:
                           id = User.objects.filter(Q(username=request.data['username'])|Q(email=request.data['username']))[0]
                       else:
                           return Response(serializer.validated_data,status=status.HTTP_400_BAD_REQUEST)
                   else:
                       return Response({'status': 'Either username or Email is Mandatory to login'},status=status.HTTP_400_BAD_REQUEST)


               test_token       = serializer.data["tokens"]
               username         = serializer.data['username']
               test_refresh     = ast.literal_eval(test_token)
               user_data        = User.objects.filter(Q(username=request.data['username'])|Q(email=request.data ['username'])).values('email','is_verified', 'last_login')
               return Response({"username":username,'email_id':user_data[0]['email'],'is_verified':user_data[0]['is_verified'],"tokens": test_refresh, 'first_time':first_time_login}, status=status.HTTP_200_OK)
       else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





