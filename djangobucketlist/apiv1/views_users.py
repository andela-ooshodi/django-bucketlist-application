from django.contrib.auth.models import User
from apiv1.serializer import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken


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


class LoginView(ObtainAuthToken):

    """
    Returns a generated token
    """

    def post(self, request):
        """
        Returns token for a registered user
        ---
        parameters:
            - name: username
              description: username used to register
              required: true
              type: string
              paramType: form
            - name: password
              description: secret password
              required: true
              type: string
              paramType: form
        """
        response = super(LoginView, self).post(request)
        return response
