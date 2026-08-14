# TaskFlow - Quick Start Commands

## Prerequisites

Python 3.14 must be installed with the following packages:
- fastapi 0.104.1+
- uvicorn 0.24.0+
- sqlalchemy 2.0.23+
- pydantic 2.5.0+
- python-multipart 0.0.6
- email-validator

If any packages are missing, install them:
```powershell
pip install sqlalchemy==2.0.23 python-multipart==0.0.6 email-validator
```

## Starting the FastAPI Application

From the TaskFlow root directory:

```powershell
cd c:\Users\vishw\TaskFlow
cd backend
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI (Documentation)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The database file `taskflow.db` will be created automatically on first run.

### Alternative: Using Uvicorn Directly

```powershell
cd c:\Users\vishw\TaskFlow\backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Running Algorithm Tests

From the TaskFlow root directory:

```powershell
cd c:\Users\vishw\TaskFlow\tests
python test_algorithms.py
```

This runs all 15 algorithm test cases and shows:
- Test results (PASS/FAIL)
- Operation statistics
- Summary with pass rate

## Running Performance Benchmarks

From the TaskFlow root directory:

```powershell
cd c:\Users\vishw\TaskFlow\tests
python benchmark.py
```

This benchmarks insertion sort, linear search, and binary search with input sizes:
- 100 tasks
- 500 tasks  
- 1000 tasks

Output includes:
- Comparisons, assignments, swaps counts
- Execution times
- Complexity analysis
- Algorithm recommendations

## Project Structure

```
TaskFlow/
├── backend/
│   ├── main.py              (FastAPI application - START HERE)
│   ├── database.py          (SQLite configuration)
│   ├── models.py            (SQLAlchemy ORM models)
│   ├── schemas.py           (Pydantic validation)
│   ├── crud.py              (Database operations)
│   ├── algorithms.py        (Sorting and search)
│   ├── ai_parser.py         (Natural language parser)
│   └── requirements.txt
├── tests/
│   ├── test_algorithms.py   (Unit tests)
│   └── benchmark.py         (Performance benchmarks)
├── frontend/                (HTML/CSS/JS - not required for API testing)
└── COMPLETION_SUMMARY.md    (Detailed documentation)
```

## API Usage Examples

### Create a User
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'
```

### Get Users
```bash
curl http://localhost:8000/users/
```

### Create a Project
```bash
curl -X POST http://localhost:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "owner_id": 1}'
```

### Create a Task
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Important task", "priority": "high", "project_id": 1, "creator_id": 1}'
```

### Search Tasks
```bash
curl "http://localhost:8000/tasks/search?title=task&algo=linear"
curl "http://localhost:8000/tasks/search?title=task&algo=binary"
```

### Get Statistics
```bash
curl http://localhost:8000/stats/aggregate
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'sqlalchemy'"
Run: `pip install sqlalchemy==2.0.23`

### "ModuleNotFoundError: No module named 'email_validator'"
Run: `pip install email-validator`

### "Address already in use" error
Change the port in the uvicorn command:
```powershell
python main.py  # Changes port to 8001, 8002, etc. automatically
# OR
uvicorn main:app --port 8001
```

### Database permission issues
Ensure the backend directory is writable. The taskflow.db file will be created there.

## Documentation Files

- **COMPLETION_SUMMARY.md** - Complete project documentation
- **backend/algorithms.py** - Algorithm documentation
- **backend/ai_parser.py** - Task parser documentation
- **tests/test_algorithms.py** - Test documentation
- **tests/benchmark.py** - Benchmark documentation

## File Status

✓ All Python files: Syntax verified
✓ All imports: Verified and circular imports avoided
✓ Database: Automatic creation on startup
✓ Models: SQLAlchemy 2.x compatible
✓ Schemas: Pydantic v2 compatible
✓ Algorithms: All three algorithms implemented
✓ Tests: 15 test cases ready
✓ Benchmarks: Performance analysis ready

