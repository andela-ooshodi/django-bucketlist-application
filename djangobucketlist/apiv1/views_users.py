from django.contrib.auth.models import User
from apiv1.serializer import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class UsersView(generics.ListAPIView):

    """
    List all users
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersDetailView(generics.RetrieveAPIView):

    """
    List a user
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
