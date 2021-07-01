from django.contrib.auth.models import User
from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.response import Response
from users.models import Profile

#! queryset i serializer class można sparametryzować metodami self.get_query_set/get_serializer_class
# Flaga permissions/groups (lepiej groups)
# thunderclient -> dodatek na vscode


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = Profile.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


class SampleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {'message': 'Sample protected view'}
        return Response(content)


class RegistrationView(views.APIView):
    def post(self, request, format=None):
        user_serializer = RegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)

        else:
            return Response(user_serializer.errors)