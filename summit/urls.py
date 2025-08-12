from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('speakers/', views.speakers, name='speakers'),
    path('sponsorship/', views.sponsorship, name='sponsorship'),
    path('nominations/', views.nominations, name='nominations'),
    path('nomination-success/', views.nomination_success, name='nomination_success'),
]