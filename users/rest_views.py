from django.contrib.auth.models import User
from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response

#! queryset i serializer class można sparametryzować metodami self.get_query_set/get_serializer_class

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticated]


class SampleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {'message': 'Sample protected view'}
        return Response(content)

