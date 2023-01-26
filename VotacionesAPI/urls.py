from django.contrib import admin
from django.urls import path, include
from GlobalApi import routers
from GlobalApi.views.auth_token_views import Login, Logout, UserToken


urlpatterns = [
    path('admin/', admin.site.urls),
    path('modulos/', include('GlobalApi.routers')),
    path('', Login.as_view(), name='login'),
    path('refresh-token/', UserToken.as_view(), name='refresh-token'),
    path('logout/', Logout.as_view(), name='logout'),
]
