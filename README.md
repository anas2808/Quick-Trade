# QuickTrade

QuickTrade is a Django-based marketplace application.

## Local development (SQLite — no online database)

The local setup uses a local SQLite database file named `db.sqlite3`. It does not need Neon, PostgreSQL, or Vercel database credentials.

### Requirements

- Python 3.10 or newer (Python 3.11 is a good choice)
- Git

### 1. Clone the repository and switch to development

```bash
git clone https://github.com/anas2808/Quick-Trade.git
cd Quick-Trade
git switch development
```

If you already cloned the project, run `git switch development` from its folder.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure local environment

Copy `.env.example` to `.env`. On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

The example configuration sets `DJANGO_USE_SQLITE=true`, which forces the local SQLite database even if a PostgreSQL `DATABASE_URL` happens to exist in your shell environment. Do not put production database credentials in this local `.env` file.

### 5. Create the local database

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

Open http://127.0.0.1:8000/ in your browser. The Django admin is at http://127.0.0.1:8000/admin/.

### Local data and uploads

- Local database: `db.sqlite3` in the project root.
- Uploaded profile/listing images: stored under `media/` on your laptop.
- Local database/users/listings/uploads are separate from the live site's data.
- `db.sqlite3`, `.env`, virtual environments, and local media are ignored by Git.

### Troubleshooting

- **It connects to PostgreSQL unexpectedly:** check that your local `.env` contains `DJANGO_USE_SQLITE=true`, then restart the server.
- **Missing module errors:** activate `.venv` and run `pip install -r requirements.txt`.
- **Static files directory error:** ensure the repository contains the `static/` directory expected by the project.
- **Need a clean local database:** stop the server, back up anything important, delete `db.sqlite3`, then run `python manage.py migrate` again. This deletes local development data only.

## Deployment note

The production/Vercel configuration continues to use PostgreSQL when a supported database URL is configured. SQLite is intended for local laptop development; it is not a persistent database for Vercel serverless deployments. Do not run production migrations or test data changes against the live database while developing.
