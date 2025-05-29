# TaskFlow API Documentation

TaskFlow is a task management system that allows users to create projects, manage tasks, and collaborate with team members.

## Features

- User authentication and authorization
- Project management (create, read, update, delete)
- Task management with status and priority tracking
- Team collaboration through project membership
- Task assignment and status updates

## API Endpoints

### Authentication

#### Register a new user

- **Method**: POST
- **Endpoint**: `/api/register/`
- **Request Body**:

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "password2": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

- **Response**: 201 Created

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Get/Update User Profile

- **Method**: GET/PUT
- **Endpoint**: `/api/user/`
- **Authentication**: Required
- **Request Body (PUT)**:

```json
{
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software Developer"
}
```

- **Response**: 200 OK

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software Developer"
}
```

### Projects

#### List/Create Projects

- **Method**: GET/POST
- **Endpoint**: `/api/projects/`
- **Authentication**: Required
- **Request Body (POST)**:

```json
{
  "title": "Web Application Development",
  "description": "Building a new web application",
  "member_ids": [2, 3]
}
```

- **Response**: 200 OK (GET), 201 Created (POST)

```json
{
  "id": 1,
  "title": "Web Application Development",
  "description": "Building a new web application",
  "owner": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "members": [
    {
      "id": 2,
      "username": "janedoe",
      "email": "jane@example.com"
    }
  ],
  "created_at": "2024-03-14T12:00:00Z",
  "updated_at": "2024-03-14T12:00:00Z"
}
```

#### Get/Update/Delete Project

- **Method**: GET/PUT/DELETE
- **Endpoint**: `/api/projects/{id}/`
- **Authentication**: Required
- **Request Body (PUT)**:

```json
{
  "title": "Updated Project Title",
  "description": "Updated project description",
  "member_ids": [2, 3, 4]
}
```

- **Response**: 200 OK (GET/PUT), 204 No Content (DELETE)

### Tasks

#### List/Create Tasks

- **Method**: GET/POST
- **Endpoint**: `/api/tasks/`
- **Authentication**: Required
- **Query Parameters (GET)**:
  - project_id: Filter tasks by project
  - status: Filter by status (TODO, IN_PROGRESS, DONE)
  - priority: Filter by priority (LOW, MEDIUM, HIGH)
  - assigned_to: Filter by assigned user ID
- **Request Body (POST)**:

```json
{
  "title": "Implement User Authentication",
  "description": "Set up JWT authentication",
  "project_id": 1,
  "assigned_to_id": 2,
  "status": "TODO",
  "priority": "HIGH",
  "due_date": "2024-03-20T18:00:00Z"
}
```

- **Response**: 200 OK (GET), 201 Created (POST)

```json
{
  "id": 1,
  "title": "Implement User Authentication",
  "description": "Set up JWT authentication",
  "project": {
    "id": 1,
    "title": "Web Application Development"
  },
  "assigned_to": {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com"
  },
  "created_by": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "status": "TODO",
  "priority": "HIGH",
  "due_date": "2024-03-20T18:00:00Z",
  "created_at": "2024-03-14T12:00:00Z",
  "updated_at": "2024-03-14T12:00:00Z"
}
```

#### Get/Update/Delete Task

- **Method**: GET/PUT/DELETE
- **Endpoint**: `/api/tasks/{id}/`
- **Authentication**: Required
- **Request Body (PUT)**:

```json
{
  "title": "Updated Task Title",
  "description": "Updated task description",
  "assigned_to_id": 2,
  "status": "IN_PROGRESS",
  "priority": "MEDIUM",
  "due_date": "2024-03-21T18:00:00Z"
}
```

- **Response**: 200 OK (GET/PUT), 204 No Content (DELETE)

#### Update Task Status

- **Method**: POST
- **Endpoint**: `/api/tasks/{task_id}/status/`
- **Authentication**: Required
- **Request Body**:

```json
{
  "status": "IN_PROGRESS"
}
```

- **Response**: 200 OK

#### Assign Task

- **Method**: POST
- **Endpoint**: `/api/tasks/{task_id}/assign/`
- **Authentication**: Required
- **Request Body**:

```json
{
  "user_id": 2
}
```

- **Response**: 200 OK

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Authentication required
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server-side error

Example error response:

```json
{
  "error": "You don't have permission to update this task"
}
```

## Authentication

All endpoints except `/api/register/` require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/taskflow.git
cd taskflow
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Project Structure

```
taskflow/
├── manage.py
├── taskflow/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - [your-email@example.com](mailto:your-email@example.com)

Project Link: [https://github.com/yourusername/taskflow](https://github.com/yourusername/taskflow)
