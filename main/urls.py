from django.urls import path

from main.views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<str:slug>/', category_detail, name='category-detail'),
    path('recipe-detail/<int:pk>/', recipe_detail, name='recipe-detail'),
    path('add-recipe/', add_recipe, name='add-recipe'),
    path('update-recipe/<int:pk>/', update_recipe, name='update-recipe'),
    path('delete-recipe/<int:pk>/', delete_recipe, name='delete-recipe'),
]