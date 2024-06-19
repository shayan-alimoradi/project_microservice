from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from project.models import Project


class ProjectTests(APITestCase):
    def setUp(self):
        self.project = baker.make(Project)

    def test_create_project_if_data_is_valid_returns_201(self):
        data = {"name": "New Project", "description": "This is a test project"}
        response = self.client.post("/api/project-create/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_create_project_if_data_is_invalid_returns_400(self):
        response = self.client.post("/api/project-create/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_projects_returns_200(self):
        response = self.client.get("/api/projects-list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_project_if_data_exists_returns_200(self):
        response = self.client.get(f"/api/project/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_project_if_data_is_valid_returns_200(self):
        response = self.client.put(
            f"/api/project/{self.project.id}/", data={"name": "new name"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project_returns_204(self):
        response = self.client.delete(f"/api/project/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
