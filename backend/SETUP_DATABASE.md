# Database Setup Guide

## Quick Start (SQLite - Recommended for Development)

SQLite requires no setup! Just start the application and it will create the database file automatically.

1. Make sure your `.env` file has:
   ```
   DATABASE_URL=sqlite:///./parking.db
   ```

2. Start the application - the database will be created automatically.

## PostgreSQL Setup (For Production)

### Option 1: Using Docker (Easiest)

```bash
docker run --name parking-postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=parking_db \
  -p 5432:5432 \
  -d postgres:14
```

Then update your `.env`:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/parking_db
```

### Option 2: Local PostgreSQL Installation

1. **Install PostgreSQL:**
   - Windows: Download from https://www.postgresql.org/download/windows/
   - Mac: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql postgresql-contrib`

2. **Create Database:**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE parking_db;
   
   # Create user (optional)
   CREATE USER parking_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE parking_db TO parking_user;
   ```

3. **Update .env file:**
   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/parking_db
   ```
   Or if you created a user:
   ```
   DATABASE_URL=postgresql://parking_user:your_password@localhost:5432/parking_db
   ```

### Option 3: Cloud Database (Production)

For production, use a managed PostgreSQL service:
- **Supabase** (Free tier available): https://supabase.com
- **Railway**: https://railway.app
- **AWS RDS**: https://aws.amazon.com/rds/
- **Heroku Postgres**: https://www.heroku.com/postgres

## Troubleshooting

### "password authentication failed"

This means your PostgreSQL password is incorrect. 

1. **Reset PostgreSQL password:**
   ```bash
   # Windows (run as Administrator)
   net stop postgresql-x64-14
   # Edit pg_hba.conf to use 'trust' authentication temporarily
   # Then:
   psql -U postgres
   ALTER USER postgres WITH PASSWORD 'new_password';
   # Revert pg_hba.conf changes
   net start postgresql-x64-14
   ```

2. **Or create a new user:**
   ```sql
   CREATE USER parking_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE parking_db TO parking_user;
   ```

### "connection refused" or "could not connect"

1. **Check if PostgreSQL is running:**
   ```bash
   # Windows
   services.msc  # Look for PostgreSQL service
   
   # Mac/Linux
   sudo systemctl status postgresql
   ```

2. **Check if port 5432 is open:**
   ```bash
   # Windows
   netstat -an | findstr 5432
   
   # Mac/Linux
   lsof -i :5432
   ```

### For Development: Use SQLite

If you just want to get started quickly, use SQLite:

1. Update `.env`:
   ```
   DATABASE_URL=sqlite:///./parking.db
   ```

2. No additional setup needed! The database file will be created automatically.

## Migration from SQLite to PostgreSQL

When you're ready to move to PostgreSQL:

1. Export data from SQLite (if needed)
2. Update `.env` with PostgreSQL connection string
3. Run migrations:
   ```bash
   alembic upgrade head
   ```


