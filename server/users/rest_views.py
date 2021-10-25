from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token
from users.serializers import PasswordResetSerializer, UserSerializer, RegisterUserSerializer
from .tasks import send_activation_email_task

#! queryset i serializer class można sparametryzować metodami self.get_query_set/get_serializer_class
# Flaga permissions/groups (lepiej groups)
# thunderclient -> dodatek na vscode


class UserViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# uuid4 - standard tworzenia id, generuje losowy ciąg znaków


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        user = serializer.save(user=self.request.user)
# wzorzec obserwator
        current_site = get_current_site(self.request)
        print(f'User email -------> "{user.email}"')
        send_activation_email_task.delay(
            current_site.domain,
            urlsafe_base64_encode(force_bytes(user.pk)),
            user.email,
            account_activation_token.make_token(user)
        )

# domain.com/subdomain/<id>
# domain.com/subdomain?id=<id>
# 19.10: 16:30


class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        user_id = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=user_id)

        if user and account_activation_token.check_token(user, token):
            user.profile.email_verified = True
            user.save()
            return Response({
                "profile": "Account has been activated"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "User does not exists or invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {'request': self.request}
