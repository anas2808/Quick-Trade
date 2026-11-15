# QuickTrade

QuickTrade is a Django-based marketplace application where users can browse second-hand product listings, create an account, publish items for sale, manage their listings, and communicate with other users. The project also includes a custom administration area for managing categories, users, and listings.

**Repository:** https://github.com/anas2808/Quick-Trade

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
- Custom administration dashboard for category, user, and listing management
- Product and profile image uploads

## Local development (SQLite — no online database)

The recommended laptop setup uses a local SQLite database file named `db.sqlite3`. It does not need Neon, PostgreSQL, or Vercel database credentials. The local `.env.example` configuration uses `DJANGO_USE_SQLITE=true` to explicitly select SQLite, even if a PostgreSQL `DATABASE_URL` is present in your shell environment.

### Requirements

- Python 3.10 or newer (Python 3.11 is a good choice)
- Git
- A terminal (PowerShell on Windows, Terminal on macOS/Linux)

Check your installations:

```bash
python --version
git --version
```

On some systems, use `python3` instead of `python`.

### 1. Clone the repository and switch to development

```bash
git clone https://github.com/anas2808/Quick-Trade.git
cd Quick-Trade
git switch development
```

If you already cloned the project, run `git switch development` from its folder.

### 2. Create and activate a virtual environment

A virtual environment keeps this project's Python packages separate from other projects.

**Windows PowerShell:**

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\\Scripts\\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure local environment

Copy `.env.example` to `.env`.

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**

```bash
cp .env.example .env
```

The example configuration sets `DJANGO_USE_SQLITE=true`, which forces the local SQLite database even if a PostgreSQL `DATABASE_URL` happens to exist in your shell environment. Do not put production database credentials in this local `.env` file. Keep `.env` private and do not commit it to GitHub.

### 5. Create the local database

Run the existing Django migrations:

```bash
python manage.py migrate
```

Create your own local admin account if needed:

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

- **Local website:** http://127.0.0.1:8000/
- **Custom administration login:** http://127.0.0.1:8000/admin/login/

The project uses a custom administration area under `/admin/`; Django's built-in admin route is not enabled in the current URL configuration.

To stop the server, press `Ctrl + C` in the terminal.

## Run it again later

Whenever you want to work on the project again:

1. Open the project folder in your terminal or editor.
2. Activate the virtual environment.
3. Start the server.

For example, on Windows PowerShell:

```powershell
cd Quick-Trade
.\\.venv\\Scripts\\Activate.ps1
python manage.py runserver
```

On macOS/Linux:

```bash
cd Quick-Trade
source .venv/bin/activate
python manage.py runserver
```

## Local data and uploads

- Local database: `db.sqlite3` in the project root.
- Uploaded profile and listing images: stored under `media/` on your laptop.
- Your local database, users, listings, and uploads are separate from the live site's data.
- `db.sqlite3`, `.env`, virtual environments, and local media are ignored by Git.

## Project structure

```text
Quick-Trade/
├── Quick_Trade/             # Django settings, URLs, middleware, and WSGI
├── Quick_Trade_Client/      # User accounts, products, messages, and client views
│   └── migrations/          # Database migrations
├── Quick_Trade_admin/       # Custom administration views and functionality
├── templat/                 # Django HTML templates
├── static/                  # CSS, JavaScript, and static assets
├── staticfile/              # Collected static files (deployment output)
├── media/                   # Uploaded product and profile images
├── db.sqlite3               # Local SQLite database file (created/used locally)
├── manage.py                # Django management commands
├── requirements.txt         # Python dependencies
├── Procfile                 # Gunicorn start command
└── vercel.json              # Vercel build and function configuration
```

## Useful Django commands

Run these from the project root with the virtual environment activated:

```bash
# Start the local server
python manage.py runserver

# Apply database migrations
python manage.py migrate

# Create migrations after changing models
python manage.py makemigrations

# Create a local superuser
python manage.py createsuperuser

# Run project tests
python manage.py test

# Collect static files (mainly for deployment)
python manage.py collectstatic
```

## Troubleshooting

- **It connects to PostgreSQL unexpectedly:** check that your local `.env` contains `DJANGO_USE_SQLITE=true`, then restart the server.
- **Missing module errors:** activate `.venv` and run `pip install -r requirements.txt`.
- **Static files directory error:** ensure the repository contains the `static/` directory expected by the project.
- **Host or `DisallowedHost` errors:** check the local `DJANGO_ALLOWED_HOSTS` setting in your `.env` file and restart the server.
- **PowerShell blocks virtual environment activation:** use Command Prompt and run `.venv\\Scripts\\activate.bat`, or allow activation for the current PowerShell process only.
- **Need a clean local database:** stop the server, back up anything important, delete `db.sqlite3`, then run `python manage.py migrate` again. This deletes local development data only.

## Database and deployment notes

- **Local development:** SQLite is selected explicitly by `DJANGO_USE_SQLITE=true` in the example local environment configuration.
- **Vercel deployment:** the settings use a configured PostgreSQL connection URL. Supported environment variable names include `DATABASE_URL`, `POSTGRES_URL`, `POSTGRES_PRISMA_URL`, and `POSTGRES_URL_NON_POOLING`.
- **Production secret:** set `DJANGO_SECRET_KEY` to a private, randomly generated value. Never commit secrets to GitHub.
- **Debug mode:** keep `DJANGO_DEBUG=False` in production.
- **Uploaded files:** the local `media/` directory stores uploads during laptop development. Vercel's serverless filesystem is not persistent, so production uploads need persistent object storage if they must survive deployments and function instances.
- **Database file:** removing `db.sqlite3` and running migrations creates a fresh local database without existing sample records. Back up the file first if you need its data.

## Contributing

1. Switch to or create a feature branch from `development`.
2. Make and test your changes locally.
3. Commit your changes to your branch.
4. Open a pull request targeting `development`.

---

Developed as the **QuickTrade** project.
