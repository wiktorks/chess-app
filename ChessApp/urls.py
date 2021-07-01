from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),  
    # path('auth/', include(router.urls))
    path('sample/', include('users.urls'))
]
