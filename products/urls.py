from django.urls import path
from rest_framework import routers

from .views import *


urlpatterns = [
    path('create/', ProductCreateAPIView.as_view()),
    path('<int:pk>/', ProductDetailAPIView.as_view()),
]