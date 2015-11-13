from django.contrib.auth.models import User
from apiv1.serializer import UserSerializer
from rest_framework import generics


class UsersView(generics.ListAPIView):

    """
    List all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersDetailView(generics.RetrieveAPIView):

    """
    List a users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
