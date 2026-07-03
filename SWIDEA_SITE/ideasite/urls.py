from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "ideasite" 

urlpatterns = [
    path("", views.idea_list, name="list"),
    path("register/", views.idea_register, name="register"),
    path("detail/<int:idea_id>/", views.idea_detail, name="detail"),
    path("edit/<int:idea_id>/", views.idea_edit, name="edit"),
    path("delete/<int:idea_id>/", views.idea_delete, name="delete"),
    path("devtool/", views.devtool_list, name="devtool_list"),
    path("devtool/register", views.devtool_register, name="devtool_register"),
    path("devtool/detail/<int:devtool_id>/", views.devtool_detail, name="devtool_detail"),
    path("devtool/edit/<int:devtool_id>/", views.devtool_edit, name="devtool_edit"),
    path("devtool/delete/<int:devtool_id>/", views.devtool_delete, name="devtool_delete"),

    path("interest/<int:idea_id>/", views.idea_interest, name="idea_interest"),
    path("star/<int:idea_id>/", views.idea_star, name="idea_star"),
]

# 이미지 저장하기 위해서 필요
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)