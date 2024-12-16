from django.contrib import admin
from django.urls import path, include, re_path  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('WebApplication.urls')),
    path('admin_tools/', include('admin_tools.urls')),
]
