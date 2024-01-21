from django.urls import path
from . import views


urlpatterns = [
    
    path('login', views.userLogin, name='userlogin'),
    path('logout', views.userLogout, name='userlogout'),
    path('register', views.userRegister, name='userregister'),
    path('', views.home, name='home'),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('update_profile/<str:pk>/', views.update_userProfile, name='update_profile'),
    
    path('create_room/', views.create_room, name='create_room'),
    path('room/<str:pk>/', views.room, name='room'),
    path('update_room/<str:pk>/', views.update_room, name='update_room'),
    path('delete_room/<str:pk>/', views.DeleteRoom, name='delete_room'),
    path('delete_massage/<str:pk>/', views.DeleteMassage, name='delete_massage'),
]