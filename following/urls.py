from django.urls import path

from . import views

urlpatterns = [
    path('api/create_user/', views.create_user),
    path('api/follow_user/', views.follow_user),
    path('api/unfollow_user/', views.unfollow_user),
]
