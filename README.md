# TaskFlow - Full-Stack Task & Project Management System

A modern full-stack task and project management application built with FastAPI, SQLAlchemy, and vanilla JavaScript.

## Project Structure

```
TaskFlow/
├── backend/              # FastAPI backend application
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── database.py      # Database configuration and session management
│   ├── crud.py          # CRUD operations for all entities
│   ├── algorithms.py    # Search and sort algorithms with counting wrappers
│   └── requirements.txt # Python dependencies
├── frontend/            # Frontend application
│   ├── index.html      # Main HTML file
│   ├── style.css       # CSS styling
│   └── script.js       # JavaScript logic
├── utils/              # Utility scripts
│   ├── check_algorithms.py    # Algorithm validation script
│   ├── benchmarks.py          # Performance benchmarking script
│   └── ai_task_parser.py      # AI quick task parser
└── README.md           # This file
```

## Features

### Backend
- **FastAPI** for high-performance API
- **SQLAlchemy ORM** with SQLite database
- **Pydantic** for data validation
- **CORS** support for frontend communication
- **Request timing middleware** for performance monitoring
- **Database relationships**: Users → Projects → Tasks

### Database Schema
- **Users**: Email (unique), created_at timestamp
- **Projects**: Name, description, owner_id (FK to users)
- **Tasks**: Title, description, priority (low/medium/high), project_id (FK to projects), due_date (nullable)

### Algorithms
- **Insertion Sort**: In-place sorting with operation counting
- **Binary Search**: Efficient searching on sorted data
- **Linear Search**: Straightforward sequential search
- **GET /tasks?sort=priority**: Sort tasks using insertion sort
- **GET /tasks/search**: Search with selectable algorithm (binary/linear)

### Frontend
- Clean, modern interface for task and project management
- Create, read, update, delete operations
- Task filtering and sorting
- Project organization
- Real-time statistics

## Getting Started

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

Simply open `frontend/index.html` in your browser. The frontend will connect to the backend API automatically.

## API Endpoints

### Users
- `POST /users/` - Create a user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user details

### Projects
- `POST /projects/` - Create a project
- `GET /projects/` - List all projects
- `GET /projects/{project_id}` - Get project details

### Tasks
- `POST /tasks/` - Create a task
- `GET /tasks/` - List all tasks
- `GET /tasks?sort=priority` - List tasks sorted by priority
- `GET /tasks/search?title=...&algo=binary|linear` - Search tasks with specified algorithm
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### Statistics
- `GET /stats/aggregate` - Get aggregate statistics

## Testing & Validation

Run the checking script to validate algorithms:
```bash
python utils/check_algorithms.py
```

Run benchmarks with multiple input sizes:
```bash
python utils/benchmarks.py
```

Run the AI task parser:
```bash
python utils/ai_task_parser.py
```

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: RESTful with CORS support

## Development

The project uses:
- FastAPI's automatic OpenAPI documentation
- SQLAlchemy for ORM relationships
- Pydantic for data validation
- CORS middleware for cross-origin requests
- Custom request timing middleware

## License

MIT
