from django.contrib import admin
from django.urls import path, include
from GlobalApi import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('modulos/', include('GlobalApi.routers')),
]
