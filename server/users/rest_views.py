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
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token
from users.serializers import UserSerializer, RegisterUserSerializer
from .tasks import send_activation_email_task, send_email_task_test

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

# uuid4 - standard tworzenia id, generuje losowy ciąg znaków 
class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
# wzorzec obserwator
        current_site = get_current_site(self.request)
        send_activation_email_task.delay(
            current_site,
            urlsafe_base64_encode(force_bytes(user.pk)),
            account_activation_token.make_token(user),
            user.email
        )

# domain.com/subdomain/<id>
# domain.com/subdomain?id=<id>
# 19.10: 16:30

class ActivateAccountView(APIView):
    def post(self, request):
        pass


class TestMessageView(APIView):
    def get(self, request, format=None):
        send_email_task_test.delay()
        return Response({
            'message': f'My current site: {get_current_site(request)}'
        })
