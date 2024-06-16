from django.core.cache import cache
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Project
from .serializers import ProjectSerializer


class ProjectListAPIView(APIView):
    """
    Return a list of all projects.
    The list is cached to reduce database load.
    """

    def get(self, request):
        # Attempt to fetch projects from cache
        projects = cache.get("projects_list")

        if not projects:
            # If not cached, fetch from database
            projects = Project.objects.all()
            # Cache the result for CACHE_TIMEOUT seconds
            cache.set("projects_list", projects, timeout=settings.CACHE_TIMEOUT)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectCreateAPIView(APIView):
    """
    Create a new project.
    The cache is invalidated after creating a new project.

    Input data => { \n
        "name": "str", \n
        "description": "str"
    }
    """

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate cache after creating a new project
            cache.delete("projects_list")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        """
        Retrieve the details of a specific project by its ID.

        Args:
            pk (int): The primary key of the project.
        """
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update the details of a specific project by its ID.
        The cache is invalidated after updating the project.

        Args:
            pk (int): The primary key of the project.

        Input data => { \n
            "name": "str", \n
            "description": "str"
        }
        """
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate cache after updating project
            cache.delete("projects_list")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific project by its ID.
        The cache is invalidated after deleting the project.

        Args:
            pk (int): The primary key of the project.
        """
        project = self.get_object(pk)
        project.delete()
        # Invalidate cache after deleting project
        cache.delete("projects_list")
        return Response(status=status.HTTP_204_NO_CONTENT)
