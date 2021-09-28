from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import permissions
from django.contrib.auth.models import User

from users.serializers import UserSerializer, RegisterUserSerializer
from users.models import Profile

#! queryset i serializer class można sparametryzować metodami self.get_query_set/get_serializer_class
# Flaga permissions/groups (lepiej groups)
# thunderclient -> dodatek na vscode


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
class GenericAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin
):
'''
# JWT Auth
class ModifyUserView(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def patch(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     serializer_class = UserSerializer
#     queryset = Profile.objects.all()
#     # permission_classes = [permissions.IsAuthenticated]


# class SampleView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         content = {'message': 'Sample protected view'}
#         return Response(content)


# # Spróbuj też mixinem

# class RegistrationView(views.APIView):
#     def post(self, request, format=None):
#         user_serializer = RegistrationSerializer(data=request.data)
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return Response(user_serializer.data)

#         else:
#             return Response(user_serializer.errors)
