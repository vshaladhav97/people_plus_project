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
               user_data        = User.objects.filter(Q(username=request.data['username'])|Q(email=request.data ['username'])).values('email',)
               return Response({"username":username,'email_id':user_data[0]['email'],"tokens": test_refresh}, status=status.HTTP_200_OK)
       else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Fetch User Profile API View
class UserProfileAPIView(generics.GenericAPIView):
    def get(self, request):
        json_data                   = request.data
        user_id                     = request.user.id
        user_data                   = User.objects.get(id = user_id)
        user_dict                   = {}
        user_dict["id"]             = user_data.id
        user_dict["username"]       = user_data.username
        user_dict["email"]          = user_data.email
        user_dict["first_name"]     = user_data.first_name if user_data.first_name else ""
        user_dict["last_name"]      = user_data.last_name if user_data.last_name else ""
        user_dict["dob"]            = user_data.dob if user_data.dob else ""
        user_dict["gender"]         = user_data.gender if user_data.gender else ""
        user_dict["profile_image"]  = user_data.profile_image.url if user_data.profile_image else ""
        return Response({'result' : user_dict}, status=status.HTTP_200_OK)

        # # 1. List all
        #
        #
        # user_fetch = User.objects.filter(id=request.user.id)
        # serializer = UserFetchSerializer(user_fetch, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

# User List API View
class UserListAPIView(generics.GenericAPIView):
    def get(self, request):
        user_data = User.objects.all()
        users_list = []
        if user_data:
            for users in user_data:
                user_dict = {}
                user_dict['user_id']        = users.id
                user_dict['username']       = users.username
                user_dict['profile_image']  = users.profile_image.url if users.profile_image else ""
                users_list.append(user_dict)
            return Response({'result': users_list}, status=status.HTTP_200_OK)
        else:
            return Response({'result': users_list}, status=status.HTTP_204_NO_CONTENT)

# User Followed and Followers API View
class UserFollowedAndFollowersListAPIView(generics.GenericAPIView):
    def get(self, request, pk):
        user_id     = pk
        try:
            user_data   = UserFollowerAndFollowed.objects.get(user_id = user_id)
            if user_data:
                followers_dict                  = {}
                followers_dict['user_id']       = user_id
                followers_dict['followers']     = user_data.followers.all().count() if user_data.followers.all() else 0
                followers_dict['followed']      = user_data.followed.all().count() if user_data.followed.all() else 0
                return Response({'result': followers_dict}, status=status.HTTP_200_OK)
        except Exception as e:
            followers_dict                  = {}
            followers_dict['user_id']       = user_id
            followers_dict['followers']     = 0
            followers_dict['followed']      = 0
            return Response({'result': followers_dict}, status=status.HTTP_200_OK)

# User Followers Details List API View
class UserFollowerDetailsListAPIView(generics.GenericAPIView):
    def get(self, request, pk):
        try:
            user_id     = pk
            user_data   = UserFollowerAndFollowed.objects.get(user_id=user_id)
            followers_list = []
            if user_data:
                # followers_dict                  = {}
                # followers_dict['followers']     = user_data.followers.all().count() if user_data.followers.all() else 0
                for users in user_data.followed.all():
                    followers_dict = {}
                    followers_dict['user_id'] = users.id
                    followers_dict['username'] = users.username
                    followers_dict['profile_image'] = users.profile_image.url if users.profile_image else ""
                    
                    followers_list.append(followers_dict)
                return Response({'result': followers_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'result': e.args}, status=status.HTTP_400_BAD_REQUEST)

# User Followed Details List API View
class UserFollowedDetailsListAPIView(generics.GenericAPIView):
    def get(self, request, pk):
        try:
            user_id = pk
            user_data = UserFollowerAndFollowed.objects.get(user_id=user_id)
            followers_list = []
            if user_data:
                # followers_dict                  = {}
                # followers_dict['followers']     = user_data.followers.all().count() if user_data.followers.all() else 0
                for users in user_data.followers.all():
                    followers_dict = {}
                    followers_dict['user_id'] = users.id
                    followers_dict['username'] = users.username
                    followers_dict['profile_image'] = users.profile_image.url if users.profile_image else ""

                    followers_list.append(followers_dict)
                return Response({'result': followers_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'result': e.args}, status=status.HTTP_400_BAD_REQUEST)




