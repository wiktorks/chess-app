from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.rest_views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('auth/', include(router.urls))
]
