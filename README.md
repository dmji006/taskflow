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
  "last_name": "Doe",
  "photo": "file (optional)"
}
```

- **Notes**:
  - Photo must be less than 2MB
  - Supported formats: JPG, JPEG, PNG, WebP
- **Response**: 201 Created

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "photo": "string (URL)"
}
```

#### Get Token

- **Method**: POST
- **Endpoint**: `/api/token/`
- **Request Body**:

```json
{
  "username": "string",
  "password": "string"
}
```

- **Response**: 200 OK

```json
{
  "access": "string",
  "refresh": "string"
}
```

#### Refresh Token

- **Method**: POST
- **Endpoint**: `/api/token/refresh/`
- **Request Body**:

```json
{
  "refresh": "string"
}
```

- **Response**: 200 OK

```json
{
  "access": "string"
}
```

### Get/Update User Profile

- **Method**: GET/PUT
- **Endpoint**: `/api/user/`
- **Authentication**: Required
- **Request Body (PUT)**:

```json
{
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software Developer",
  "photo": "file (optional)"
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
  "photo": "string (URL)",
  "is_active": true,
  "date_joined": "2025-06-01T12:00:00Z",
  "last_login": "2025-06-03T12:00:00Z"
}
```

### Tasks

#### List/Create Tasks

- **Method**: GET/POST
- **Endpoint**: `/api/tasks/`
- **Authentication**: Required
- **Query Parameters (GET)**:
  - status: Filter by status (TODO, IN_PROGRESS, DONE)
  - priority: Filter by priority (LOW, MEDIUM, HIGH)
  - created_by: Filter by creator user ID (admin only)
- **Request Body (POST)**:

```json
{
  "title": "Implement User Authentication",
  "description": "Set up JWT authentication",
  "assigned_to_id": 2,
  "status": "TODO",
  "priority": "HIGH"
}
```

- **Response**: 200 OK (GET), 201 Created (POST)

```json
{
  "id": 1,
  "title": "Implement User Authentication",
  "description": "Set up JWT authentication",
  "assigned_to": "janedoe",
  "created_by": 1,
  "status": "TODO",
  "priority": "HIGH",
  "created_at": "2024-03-14T12:00:00Z",
  "updated_at": "2024-03-14T12:00:00Z",
  "comments": []
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
  "priority": "MEDIUM"
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

#### Task Comments

- **Method**: POST
- **Endpoint**: `/api/tasks/{task_id}/comments/`
- **Authentication**: Required
- **Description**: Add a comment to a task (only task creator and assigned user can comment)
- **Request Body**:

```json
{
  "content": "string"
}
```

- **Response**: 201 Created

```json
{
  "id": 1,
  "task": 1,
  "user": "johndoe",
  "content": "string",
  "created_at": "2025-06-03T12:00:00Z",
  "updated_at": "2025-06-03T12:00:00Z"
}
```

#### Delete Comment

- **Method**: DELETE
- **Endpoint**: `/api/comments/{comment_id}/`
- **Authentication**: Required
- **Description**: Delete a comment (only comment creator and admins can delete)
- **Response**: 200 OK

```json
{
  "message": "Comment deleted successfully"
}
```

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

4. Set up PostgreSQL:

   - Install PostgreSQL if not already installed
   - Create a new database named 'taskflow'
   - Update database settings in taskflow/settings.py if needed

5. Apply database migrations:

```bash
python manage.py migrate
```

6. Create an admin user:

```bash
python manage.py createsuperadmin
```

- Default credentials: username=admin, password=admin123
- You can create additional superusers with:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Project Structure

```
taskflow/
├── manage.py
├── requirements.txt
├── README.md
├── media/
│   └── user_photos/
├── taskflow/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── myapp/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       ├── utils.py
│       ├── views.py
│       ├── management/
│       │   └── commands/
│       │       └── createsuperadmin.py
│       └── migrations/
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

## Rate Limiting

The API implements rate limiting to prevent abuse. Each client is limited to:

- 5 requests per 60 seconds for most endpoints

When a rate limit is exceeded, the API will respond with:

- Status code: `429 Too Many Requests`
- Response body:

```json
{
  "error": "Too many requests. Please try again later.",
  "retry_after_seconds": 42
}
```

Rate limit headers are included in all responses:

- `X-RateLimit-Limit`: Maximum number of requests allowed in the time window
- `X-RateLimit-Remaining`: Number of requests remaining in the current time window
- `Retry-After`: Seconds to wait before making another request (only included in 429 responses)

### Rate Limited Endpoints

The following endpoints are subject to rate limiting:

- POST `/api/register/` - User registration
- GET/POST `/api/tasks/` - List and create tasks
- GET/PUT/DELETE `/api/tasks/{id}/` - Task details, updates, and deletion

## Admin Endpoints

### List Users (Admin Only)

- **Method**: GET
- **URL**: `/api/users/`
- **Description**: Get list of all users (admin only)
- **Headers**:
  - Authorization: Bearer {access_token}
- **Response**: 200 OK
  ```json
  {
    "count": "integer",
    "results": [
      {
        "id": "integer",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "photo": "string (URL)",
        "is_active": "boolean",
        "date_joined": "datetime",
        "last_login": "datetime"
      }
    ]
  }
  ```

### Delete User (Admin Only)

- **Method**: DELETE
- **URL**: `/api/admin/users/{user_id}/delete/`
- **Description**: Delete a user (admin only)
- **Headers**:
  - Authorization: Bearer {access_token}
- **Response**: 200 OK
  ```json
  {
    "message": "User username has been deleted successfully"
  }
  ```

### Bulk Delete (Admin Only)

- **Method**: DELETE
- **URL**: `/api/admin/bulk-delete/`
- **Description**: Delete multiple users and/or tasks (admin only)
- **Headers**:
  - Authorization: Bearer {access_token}
- **Request Body**:
  ```json
  {
    "user_ids": ["integer"],
    "task_ids": ["integer"]
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "message": "Bulk deletion completed",
    "deleted_counts": {
      "users": "integer",
      "tasks": "integer"
    }
  }
  ```
