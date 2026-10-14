# FretMate

A web practice and skill-analytics dashboard for guitarists.

## Setup
1. Clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install django psycopg dj-database-url python-dotenv
   ```
3. Copy `.env.example` to `.env` and configure your database URL.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Seed demo data (optional):
   ```bash
   python manage.py seed_data
   ```
6. Run the server:
   ```bash
   python manage.py runserver
   ```

## Production Notes
- Use a production-ready WSGI server like Gunicorn or Daphne.
- Configure `SECRET_KEY`, `ALLOWED_HOSTS`, and `DATABASE_URL` in your environment.
- Use Supabase connection pooling for PostgreSQL.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
