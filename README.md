# Advanced Project Management Microservice

This microservice is part of an advanced project management application designed with a microservices architecture, asynchronous task processing, and real-time notifications.

## Features

- **Django Project Setup**: Initializes a Django project with PostgreSQL as the primary database.
- **Project Model**: Includes fields for id, name, description, created_at, and updated_at.
- **API Endpoints**: Implements CRUD operations for projects.
- **Redis Caching**: Utilizes Redis for caching project data to optimize performance.
- **Docker Containerization**: Provides Dockerfiles and docker-compose.yml for easy deployment.
- **Asynchronous Tasks**: Uses RabbitMQ and Celery for handling asynchronous task processing.
- **Testing**: Includes unit tests for API endpoints and caching logic.

## Setup and Installation

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/shayan-alimoradi/project_microservice
   cd project_microservice
   ```

2. Build and run the application:

    First run this command to create the project network
    ```
    docker network create project-network
    ```
    ```bash
    docker-compose up -d --build
    ```

3. Create a superuser (optional):
    ```bash
    docker exec -it project_backend python manage.py createsuperuser
    ```

4. Access the application and swagger:
    ```bash
    The API endpoints will be available at http://localhost:8000/.
    ```
    ```bash
    The swagger will be available at http://localhost:8000/swagger/.
    ```
    ```bash
    The redoc will be available at http://localhost:8000/redoc/.
    ```

    __API Endpoints__
    ```bash
    GET /api/projects-list/: List all projects.
    POST /api/project-create/: Create a new project.
    GET api/project/<id>/: Retrieve a single project by ID.
    PUT api/project/<id>/: Update a project by ID.
    DELETE api/project/<id>/: Delete a project by ID.

5. Testing

    To run tests and verify Redis caching:
    ```bash
    docker exec -it project_backend python manage.py test
    ```
    This will execute unit tests for API endpoints and caching logic.
<br/><br/>
# Integration with Task Microservice

Upon creating a project, data is published to the Task Microservice automatically.
<br/><br/>

### Feel free to extend this README with additional setup instructions or details specific to your project requirements.