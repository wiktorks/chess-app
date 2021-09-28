from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  
    # path('auth/', include(router.urls))
    path('api/auth/', include('users.urls'))
]
 