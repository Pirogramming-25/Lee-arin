from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("posts/create/", views.post_create, name="create"),
    path("posts/<int:pk>/update/", views.post_update, name="update"),
    path("posts/<int:pk>/delete/", views.post_delete, name="delete"),
    path("posts/<int:pk>/like/", views.like_toggle, name="like"),
    path("posts/<int:pk>/comments/", views.comment_create, name="comment_create"),
    path("comments/<int:pk>/update/", views.comment_update, name="comment_update"),
    path("comments/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]
