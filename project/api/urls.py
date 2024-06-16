from django.urls import path

from . import views

app_name = "api_project"


urlpatterns = [
    path("projects-list/", views.ProjectListAPIView.as_view(), name="project-list"),
    path(
        "project-create/", views.ProjectCreateAPIView.as_view(), name="project-create"
    ),
    path(
        "projects/<int:pk>/",
        views.ProjectDetailAPIView.as_view(),
        name="project-detail",
    ),
]
