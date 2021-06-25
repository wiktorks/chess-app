from django.urls import path
from django.urls.conf import include
from . import rest_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

user_router = DefaultRouter()
user_router.register('users', rest_views.UserViewSet, basename='users')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include(user_router.urls)),
    path('protected/', rest_views.SampleView.as_view(), name='protected_view')
]