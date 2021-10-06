from django.urls import path
from django.urls.conf import include
from users.rest_views import RegisterUserView, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# 
profile_router = DefaultRouter()
profile_router.register('', UserViewSet, basename='user-profile')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profiles/', include(profile_router.urls), name='user-profile'),
    path('register/', RegisterUserView.as_view(), name='user-register')
]
