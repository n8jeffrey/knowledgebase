from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_brand/', views.create_brand, name='create_brand'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('', views.home, name='home'),  # Add this line
]