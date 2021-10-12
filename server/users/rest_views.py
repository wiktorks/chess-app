from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import UserSerializer, RegisterUserSerializer
from .tasks import send_email_task

#! queryset i serializer class można sparametryzować metodami self.get_query_set/get_serializer_class
# Flaga permissions/groups (lepiej groups)
# thunderclient -> dodatek na vscode


class UserViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# POST


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


class ActivateAccountView(APIView):
    def post(self, request):
        pass


class TestMessageView(APIView):
    def get(self, request, format=None):
        send_email_task.delay()
        return Response({
            'message': 'Email has been sent to temporal mail!'
        })
