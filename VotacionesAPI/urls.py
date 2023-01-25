from django.contrib import admin
from django.urls import path, include
from GlobalApi import routers
from GlobalApi.views.auth_token_views import Login, Logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('modulos/', include('GlobalApi.routers')),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
