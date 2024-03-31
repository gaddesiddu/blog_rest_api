from django.urls import path
from .views import  post_data, update_data, delete_data, search_paragraphs


urlpatterns = [
    path('api/search/<str:word>/', search_paragraphs, name='search-paragraphs'),
    path('users/create/', post_data, name='create-user'),
    path('users/update/<int:pk>/', update_data, name='update-user'),
    path('users/delete/<int:pk>/', delete_data, name='delete-user'),
]
