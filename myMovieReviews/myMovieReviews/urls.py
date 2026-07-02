from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews_list, name='reviews-list'),
    path('create/', views.reviews_create, name='reviews-create'),
    path('<int:pk>/update/', views.reviews_edit, name='reviews-edit'),
    path('<int:pk>/read/', views.reviews_detail, name='reviews-detail'),
    path('<int:pk>/delete/', views.reviews_delete, name='reviews-delete'),
]