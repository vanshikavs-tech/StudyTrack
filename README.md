# StudyTrack - Student Task Manager

StudyTrack is a clean, simple, and beginner-friendly web application built with Python and Django. It allows students to manage their daily study tasks, track completion progress, and view task statistics.

This project was built strictly using core Django concepts (MVT pattern, built-in Authentication, ORM, and ModelForms) without any third-party APIs or JavaScript frameworks, making it easy to understand and explain in a Django viva.

---

## 1. What the Project Does

- **User Authentication**: Secure Login and Logout using Django's built-in authentication system.
- **Student Dashboard**: Shows personalized greeting, total tasks count, and completed tasks count.
- **Task Management**:
  - Add new tasks with title and description.
  - Automatically associates each task with the currently logged-in student.
  - Mark pending tasks as completed with one click.
  - Delete tasks securely using POST requests.
- **Data Isolation**: Ensures students can only view, modify, and delete their own tasks.
- **Django Admin Panel**: Allows site administrators to inspect and manage all tasks and users.

---

## 2. Technologies Used

- **Language**: Python 3
- **Framework**: Django
- **Database**: SQLite (default, zero configuration needed)
- **Frontend**: HTML5, CSS3, Django Template Language (DTL)

---

## 3. Project Structure

```
StudyTrack/
│
├── manage.py                   # Django CLI management script
├── requirements.txt            # Project dependencies
├── README.md                   # Quickstart guide
├── db.sqlite3                  # SQLite database file
│
├── studytrack/                 # Project configuration package
│   ├── __init__.py
│   ├── settings.py             # Global configurations, apps, templates, static
│   ├── urls.py                 # Main URL routing table
│   ├── wsgi.py                 # WSGI entrypoint for web servers
│   └── asgi.py                 # ASGI entrypoint for async servers
│
├── tasks/                      # Main application package
│   ├── migrations/             # Database schema migrations
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py                # Admin site configuration for Task model
│   ├── apps.py                 # App configuration
│   ├── forms.py                # ModelForm for task creation
│   ├── models.py               # Task database model
│   ├── tests.py                # Automated unit tests
│   ├── urls.py                 # App-specific URL routing
│   └── views.py                # Business logic and request handlers
│
├── templates/                  # HTML templates with Django Template Language
│   ├── base.html               # Base layout with navbar and flash messages
│   ├── login.html              # Standalone login page
│   ├── dashboard.html          # Main student dashboard with statistics & tasks
│   └── add_task.html           # Task creation form page
│
└── static/                     # Static assets
    └── style.css               # Clean, modern, responsive CSS styling
```

---

## 4. Installation & Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd fds_myproject
   ```

2. **Install Django**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## 5. How to Run the Server

Start the Django development server:
```bash
python manage.py runserver
```

Open your browser and visit:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

You will be redirected to the login page.

---

## 6. Demo Accounts & Superuser

The project comes pre-seeded with demo credentials:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Student** | `student` | `student123` | Pre-populated with 3 sample tasks |
| **Admin** | `admin` | `admin123` | Full superuser access to `/admin/` |

### How to Create a New Superuser:
If you want to create your own admin account, run:
```bash
python manage.py createsuperuser
```
Follow the interactive prompts to enter a username, email, and password.

---

## 7. Available URLs

| URL Route | View Name | Description |
| :--- | :--- | :--- |
| `/` | `root_redirect` | Automatically redirects to `/dashboard/` |
| `/login/` | `login` | Login page for students and admins |
| `/logout/` | `logout` | Logs user out and redirects to `/login/` |
| `/dashboard/` | `dashboard` | Displays student statistics and task cards |
| `/tasks/add/` | `add_task` | Form to create a new study task |
| `/tasks/<id>/complete/` | `complete_task` | Marks a specific task as completed |
| `/tasks/<id>/delete/` | `delete_task` | Deletes a task via POST |
| `/admin/` | `admin:index` | Django's built-in administration dashboard |

---

## 8. Running Automated Tests

To run the automated test suite verifying authentication, CRUD operations, statistics, and user data isolation:
```bash
python manage.py test
```
All 10 tests should pass with `OK`.

---

## 9. Viva Preparation

For a comprehensive explanation of every file, line of code, design decisions, and common viva questions, read **`VIVA_GUIDE.md`** in this directory. You can also upload `VIVA_GUIDE.md` to ChatGPT for interactive viva mock interviews!
