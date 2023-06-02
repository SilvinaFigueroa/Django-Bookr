from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:id>/', views.book_details, name='book_details'),
    path('book-search/', views.book_search, name='book_search'),
    path('publisher/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publisher/new/', views.publisher_edit, name='publisher_create'),

]
