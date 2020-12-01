from django.urls import path
from rest_framework import routers

from .views import *


urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('create/', ProductCreateAPIView.as_view()),
    path('<int:pk>/', ProductDetailAPIView.as_view()),
    path('my-products/', AuthorsProductListAPIView.as_view()),
    path('search/', SearchListView.as_view()),
    path('wishlist/', WishListApiView.as_view()),
    path('<int:pk>/wish/add/', WishAdd.as_view()),
    path('<int:pk>/wish/delete/', WishDelete.as_view()),
]