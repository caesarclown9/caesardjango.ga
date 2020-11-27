from django.urls import path

from .views import *


urlpatterns = [
    path('create/', ProductCreateAPIView.as_view()),
]