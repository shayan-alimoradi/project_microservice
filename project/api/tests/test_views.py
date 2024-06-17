from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from project.models import Project


class ProjectTests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project", description="Test Description"
        )

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
        project = baker.make(Project)
        response = self.client.get(f"/api/projects/{project.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_project_if_data_is_valid_returns_200(self):
        project = baker.make(Project)
        response = self.client.put(
            f"/api/projects/{project.id}/", data={"name": "new name"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project_returns_204(self):
        project = baker.make(Project)
        response = self.client.delete(f"/api/projects/{project.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProjectCachingTests(APITestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project", description="Test Description"
        )

    def tearDown(self):
        cache.clear()

    def test_project_list_caching(self):
        response = self.client.get("/api/projects-list/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("project_list" in cache)
        cached_response = cache.get("project_list")
        self.assertEqual(cached_response, response.data)

    def test_project_detail_caching(self):
        project = baker.make(Project)
        response = self.client.get(f"/api/projects/{project.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cache_key = f"project_{project.id}"
        self.assertTrue(cache_key in cache)
        cached_response = cache.get(cache_key)
        self.assertEqual(cached_response, response.data)

    def test_project_cache_invalidation_on_update(self):
        project = baker.make(Project)
        response = self.client.put(
            f"/api/projects/{project.id}/",
            {"name": "Updated Project", "description": "Updated Description"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cache_key = f"project_{project.id}"
        self.assertIsNone(cache.get(cache_key))

    def test_project_cache_invalidation_on_delete(self):
        project = baker.make(Project)
        response = self.client.delete(f"/api/projects/{project.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cache_key = f"project_{project.id}"
        self.assertIsNone(cache.get(cache_key))
