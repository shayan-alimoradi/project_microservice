from django.urls import path

from . import views

app_name = "api_project"


urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='project-detail'),
]