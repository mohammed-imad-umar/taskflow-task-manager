# TaskFlow — Task Manager

A responsive task management web application built with **FastAPI, Jinja2, custom CSS, Vanilla JavaScript, SQLite and SQLAlchemy ORM**.

> No Flask, Bootstrap or Tailwind CSS is used.

## Features

- Create, read, update and delete tasks (CRUD).
- Mark tasks as complete or pending.
- Filter tasks by all, in-progress and completed.
- Search task titles and descriptions.
- Set task priority (Low, Medium, High) and optional due date.
- Dashboard statistics: total, pending, completed and completion rate.
- Responsive layout and light/dark theme toggle.
- SQLite database created automatically on first run.

## Technology stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Templates | Jinja2 |
| Frontend | HTML, custom CSS, Vanilla JavaScript |
| Database | SQLite |
| ORM | SQLAlchemy 2.x |
| ASGI server | Uvicorn |

## Project structure

```text
task-manager/
├── app/
│   ├── main.py              # Routes and application entry point
│   ├── database.py          # Engine, session and DB dependency
│   ├── models.py            # SQLAlchemy Task model
│   ├── templates/           # Jinja2 HTML templates
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── requirements.txt
├── README.md
└── .gitignore
```

## Run locally

### 1. Requirements
- Python 3.10 or newer
- pip

### 2. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/taskflow-task-manager.git
cd taskflow-task-manager
```

### 3. Create and activate a virtual environment

Windows PowerShell:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 5. Start the server
```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

FastAPI's interactive API documentation is available at **http://127.0.0.1:8000/docs**.

## How the application works

1. A browser request reaches a FastAPI route in `app/main.py`.
2. The route obtains a SQLAlchemy database session using `get_db()`.
3. SQLAlchemy queries or changes the `Task` model in SQLite.
4. FastAPI passes the result to a Jinja2 template.
5. Jinja2 renders the HTML; CSS and JavaScript are served from `/static`.

## Database model

The `tasks` table contains:

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| title | String | Required task title |
| description | Text | Optional task details |
| priority | String | Low, Medium or High |
| due_date | String | Optional date (YYYY-MM-DD) |
| completed | Boolean | Completion status |
| created_at | DateTime | Creation timestamp |

The database file `task_manager.db` is generated automatically in the project root and is excluded from Git.

## CRUD mapping

| Operation | Route | Method |
|---|---|---|
| Read/list tasks | `/` | GET |
| Show create form | `/tasks/new` | GET |
| Create task | `/tasks` | POST |
| Show edit form | `/tasks/{id}/edit` | GET |
| Update task | `/tasks/{id}/edit` | POST |
| Toggle completion | `/tasks/{id}/toggle` | POST |
| Delete task | `/tasks/{id}/delete` | POST |

## Before submission

- [ ] Run the application locally and test create, list, edit, complete and delete.
- [ ] Capture screenshots or record a short walkthrough.
- [ ] Replace `YOUR-USERNAME` in the clone command if needed.
- [ ] Push the source code to your GitHub repository.
- [ ] Publish a LinkedIn post with the demo/screenshots and tag your academy/instructors.
- [ ] Submit both URLs and milestone statuses in the project tracker.

## GitHub upload

Create an empty repository on GitHub, then run:
```bash
git init
git add .
git commit -m "Build TaskFlow task manager with FastAPI and SQLAlchemy"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/taskflow-task-manager.git
git push -u origin main
```

## Learning note

This project is intended as a learning assignment. Review the route handlers, SQLAlchemy model, database dependency and Jinja2 templates so you can explain the request-to-database-to-template flow during evaluation.
