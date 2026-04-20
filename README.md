# KanMind Backend

A Django REST Framework API for a kanban board management system with user authentication, board management, task tracking, and commenting features.

## Features

- **User Authentication**: Token-based authentication with registration, login, and logout
- **Board Management**: Create and manage kanban boards with team members
- **Task Management**: Create, assign, and track tasks with status, priority, and reviewers
- **Comments**: Add and manage comments on tasks
- **Permissions**: Role-based access control (board owners, members, task creators)

## Tech Stack

- Python 3.x
- Django 6.0.4
- Django REST Framework
- SQLite (development database)
- Token Authentication

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Select Python interpreter (VS Code)**
   - Press `Ctrl + Shift + P` and select "Python: Select Interpreter"
   - Choose the Python interpreter from your virtual environment (`venv`)
   - If not listed, select "Enter interpreter path" and navigate to `venv/Scripts/python.exe` (Windows) or `venv/bin/python` (macOS/Linux)

5. **Configure environment variables**
   - Duplicate the `.env.template` file and rename it to `.env`
   - Generate a new Django secret key using one of these methods:
     
     **Option A: Using a web tool**
     - Visit https://djecrety.ir/ and copy the generated key
     
     **Option B: Using the command line**
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Paste the generated key into the `SECRET_KEY` field in your `.env` file

6. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Server

Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Project Structure

```
backend/
├── auth_app/           # User authentication and registration
├── boards/             # Board management
├── tasks/              # Task and comment management
├── core/               # Project settings and main configuration
├── manage.py           # Django management script
└── db.sqlite3          # SQLite database (created after migrations)
```

## API Endpoints

### Authentication
- `POST /api/registration/` - Register new user
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout
- `GET /api/email-check/?email={email}` - Check if email exists

### Boards
- `GET /api/boards/` - List user's boards
- `POST /api/boards/` - Create new board
- `GET /api/boards/{id}/` - Get board details
- `PATCH /api/boards/{id}/` - Update board
- `DELETE /api/boards/{id}/` - Delete board (owner only)

### Tasks
- `GET /api/tasks/` - List tasks from user's boards
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get task details
- `PATCH /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/tasks/assigned-to-me/` - List tasks assigned to user
- `GET /api/tasks/reviewing/` - List tasks user is reviewing

### Comments
- `GET /api/tasks/{task_id}/comments/` - List task comments
- `POST /api/tasks/{task_id}/comments/` - Add comment to task
- `DELETE /api/tasks/{task_id}/comments/{id}/` - Delete comment

For detailed API documentation with request/response examples, see `endpoint_testing.md`.

## Django Admin

Access the Django admin interface at `http://127.0.0.1:8000/admin/` using your superuser credentials to manage users, boards, tasks, and comments through a web interface.

## Authentication

All endpoints (except registration and login) require authentication. Include the token in the request header:

```
Authorization: Token <your-token-here>
```

Tokens are returned upon successful registration or login.

## Environment Configuration

### CORS Settings
Currently configured for frontend development:
- `localhost:5500`
- `localhost:5501`

Update `CORS_ALLOWED_ORIGINS` in `core/settings.py` for production deployment.

### Allowed Hosts
Update `ALLOWED_HOSTS` in `core/settings.py` before deploying to production.

## Database

The project uses SQLite for development. For production, configure PostgreSQL or another production database in `core/settings.py`.

### Creating New Migrations
After modifying models, create and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing

To test the API endpoints, you can use:
- **Postman** or **Thunder Client** - See `endpoint_testing.md` for a complete testing guide
- **Django Admin** - Browse and manually edit data
- **curl** or similar command-line tools

## Security Notes

- Change `SECRET_KEY` in `core/settings.py` before deploying to production
- Set `DEBUG = False` in production
- Use environment variables for sensitive configuration
- Configure proper database for production (not SQLite)

## Development

### Code Style
The codebase follows PEP 257 docstring conventions for documentation.

### Making Changes
1. Create/modify models in respective apps
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Update serializers and views as needed
5. Test endpoints using `endpoint_testing.md` guide

## License

See LICENSE.md for details.

## Authors

Created as part of the KanMind project.
