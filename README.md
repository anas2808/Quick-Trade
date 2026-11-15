# Quick-Trade

Quick-Trade is a Django-based marketplace where users can browse second-hand product listings, create an account, publish items for sale, manage their listings, and communicate with sellers. The project also includes a separate administration area for managing categories, users, and listings.

**Repository:** https://github.com/anas2808/Quick-Trade  
**Live deployment:** https://quick-trade-sigma.vercel.app

## Technology stack

- Python and Django
- SQLite for local development
- PostgreSQL for deployment when a PostgreSQL connection URL is configured
- HTML, CSS, JavaScript, and Django templates
- Pillow for image handling
- Gunicorn for WSGI serving

## Main features

- User registration, login, logout, and profile management
- Browse product listings and view product details
- Create, update, and delete product listings
- Product categories and listing status management
- User-to-user messaging
- Administration dashboard for category, user, and listing management
- Product and profile image uploads

## Requirements

Install the following before running the project:

- Python 3.10 or newer (Python 3.11 is recommended)
- Git
- A terminal (PowerShell on Windows, Terminal on macOS/Linux)

Check your installations:

```bash
python --version
git --version
```

On some systems, use `python3` instead of `python`.

## 1. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/anas2808/Quick-Trade.git
cd Quick-Trade
```

## 2. Create and activate a virtual environment

A virtual environment keeps this project's Python packages separate from other projects.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run the following in the current terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```bat
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

When the environment is active, your terminal usually displays `(venv)`.

## 3. Install project dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The dependencies are listed in `requirements.txt` and include Django, Pillow, Gunicorn, PostgreSQL support, and database URL parsing.

## 4. Configure local development

The repository's Django settings automatically use the local SQLite database (`db.sqlite3`) when no PostgreSQL URL is configured and the application is not running on Vercel. You do not need to install or configure PostgreSQL to run the project locally.

Enable Django's development mode and allow the local host.

**Windows (PowerShell):**

```powershell
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
```

**macOS / Linux:**

```bash
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

These commands set variables only for the current terminal session. If you open a new terminal, activate the virtual environment and set them again.

> The project settings contain a development fallback for Django's secret key. Do not use that fallback for a public production deployment. Configure a private `DJANGO_SECRET_KEY` in the deployment environment instead, and never commit secrets to GitHub.

## 5. Set up the database

Run the existing Django migrations to create or update the local database tables:

```bash
python manage.py migrate
```

The project includes migrations for the client application. The local database is SQLite and is stored in the project root as `db.sqlite3`.

If you want to create a new administrator account for the Django authentication system, run:

```bash
python manage.py createsuperuser
```

Follow the prompts. The custom user model uses email as its login identifier.

## 6. Run the development server

Start the local Django server:

```bash
python manage.py runserver
```

Open the application in your browser:

- **Local website:** http://127.0.0.1:8000/
- **Admin application area:** http://127.0.0.1:8000/admin/login/

The project's application routes are configured in `Quick_Trade_Client/urls.py` and `Quick_Trade_admin/urls.py`. The `/admin/` URL is the project's custom administration area; Django's built-in admin route is not enabled in the current URL configuration.

To stop the server, press `Ctrl + C` in the terminal.

## Run it again later

Whenever you want to work on the project again:

1. Open the project folder in your terminal or editor.
2. Activate the virtual environment.
3. Set the local development environment variables again.
4. Start the server.

For example, on Windows PowerShell:

```powershell
cd Quick-Trade
.\venv\Scripts\Activate.ps1
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
python manage.py runserver
```

On macOS/Linux:

```bash
cd Quick-Trade
source venv/bin/activate
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
python manage.py runserver
```

## Project structure

```text
Quick-Trade/
├── Quick_Trade/             # Django project settings, URLs, middleware, WSGI
├── Quick_Trade_Client/      # User accounts, products, messages, and client views
│   └── migrations/          # Database migrations
├── Quick_Trade_admin/       # Custom administration views and functionality
├── templat/                 # Django HTML templates
├── static/                  # CSS, JavaScript, and static assets
├── staticfile/              # Collected static files (deployment output)
├── media/                   # Uploaded product and profile images
├── db.sqlite3               # Local SQLite database file
├── manage.py                # Django management commands
├── requirements.txt         # Python dependencies
├── Procfile                 # Gunicorn start command
└── vercel.json              # Vercel build and function configuration
```

## Database and deployment notes

- **Local development:** SQLite is used automatically when no PostgreSQL URL is set and Vercel environment variables are absent.
- **Vercel deployment:** The settings require a PostgreSQL connection URL. Configure one of `DATABASE_URL`, `POSTGRES_URL`, `POSTGRES_PRISMA_URL`, or `POSTGRES_URL_NON_POOLING` in the Vercel project's environment variables.
- **Production secret:** Set `DJANGO_SECRET_KEY` to a private, randomly generated value.
- **Debug mode:** Keep `DJANGO_DEBUG=False` in production.
- **Hosts:** Configure `DJANGO_ALLOWED_HOSTS` for any custom production hostnames as needed.
- **Uploaded files:** The local `media/` directory stores uploaded files during local development. Vercel's serverless filesystem is not persistent, so production uploads need persistent object storage if they must survive deployments and function instances.
- **Database file:** The repository currently contains a `db.sqlite3` file. For a clean local database, back up that file first, then remove or rename it and run `python manage.py migrate`. This creates a fresh database; it will not contain the existing sample records.

## Troubleshooting

**1. `python` is not recognized**

Install Python and ensure it is added to your system PATH. On macOS/Linux, try `python3`.

**2. `No module named django`**

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

**3. Database or missing-table errors**

Make sure the virtual environment is active, then run:

```bash
python manage.py migrate
```

**4. Static files or images are not displaying**

Confirm that the `static/` and `media/` directories are present. For local development, ensure `DJANGO_DEBUG=True` is set in the same terminal session before starting the server.

**5. Host or `DisallowedHost` errors**

Set the local allowed hosts in the same terminal session:

```bash
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

On PowerShell, use:

```powershell
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
```

**6. PowerShell does not allow virtual environment activation**

Use the process-scoped execution policy command shown in the virtual environment section, or use Command Prompt and run `venv\Scripts\activate.bat`.

## Useful Django commands

```bash
# Start the local server
python manage.py runserver

# Apply database migrations
python manage.py migrate

# Create a new migration after changing models
python manage.py makemigrations

# Create a superuser
python manage.py createsuperuser

# Run project tests
python manage.py test

# Collect static files (mainly for deployment)
python manage.py collectstatic
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes locally.
4. Commit your changes and open a pull request.

---

Developed as the **Quick-Trade** project.
