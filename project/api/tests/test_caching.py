from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status

from project.models import Project


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
        response = self.client.get(f"/api/project/{self.project.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cache_key = f"project_{self.project.id}"
        self.assertTrue(cache_key in cache)
        cached_response = cache.get(cache_key)
        self.assertEqual(cached_response, response.data)

    def test_project_cache_invalidation_on_update(self):
        response = self.client.put(
            f"/api/project/{self.project.id}/",
            {"name": "Updated Project", "description": "Updated Description"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cache_key = f"project_{self.project.id}"
        self.assertIsNone(cache.get(cache_key))

    def test_project_cache_invalidation_on_delete(self):
        response = self.client.delete(f"/api/project/{self.project.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cache_key = f"project_{self.project.id}"
        self.assertIsNone(cache.get(cache_key))