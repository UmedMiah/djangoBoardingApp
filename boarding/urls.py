from django.urls import path
from . import views

from boarding.views import (
    user_detail_view,
    remove_access,
    index
)


urlpatterns = [
    path('', view=index, name='index'),
    path('home', view=index, name='index'),
    path('user/<str:username>', view=user_detail_view, name='user'),
    path('team', views.team, name='team'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),   
    path('logout', views.logout, name='logout'),
    path('addaccess/<str:userPK>/<str:productPK>', views.addaccess, name="addaccess"),
    path('remove/<str:pk>', view=remove_access, name="remove")
    ]