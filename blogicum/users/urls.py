from django.urls import path

from . import views

urlpatterns = [
    path('auth/registration/', views.register, name='registration'),
]
