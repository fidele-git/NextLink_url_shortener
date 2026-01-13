# Database Migration Guide: SQLite to PostgreSQL

This guide walks you through migrating your NexLink application from SQLite to PostgreSQL.

## Why PostgreSQL?

- **Production-ready**: Better performance and reliability for production environments
- **Concurrent access**: Handles multiple simultaneous connections better
- **Data integrity**: Superior constraint enforcement and ACID compliance
- **Scalability**: Better suited for growing applications
- **Advanced features**: Full-text search, JSON support, and more

## Prerequisites

- PostgreSQL installed on your system
- Backup of your current SQLite database
- Python virtual environment activated

## Step 1: Install PostgreSQL

### Windows

1. Download PostgreSQL installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer (recommended version: 14 or higher)
3. During installation:
   - Set a password for the `postgres` user (remember this!)
   - Default port: 5432
   - Install pgAdmin (optional, but helpful for GUI management)
4. Add PostgreSQL to your PATH (installer usually does this)

Verify installation:
```powershell
psql --version
```

### macOS

```bash
# Using Homebrew
brew install postgresql@14

# Start PostgreSQL
brew services start postgresql@14

# Verify installation
psql --version
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

## Step 2: Create PostgreSQL Database

### Windows

Open Command Prompt or PowerShell:

```powershell
# Connect to PostgreSQL
psql -U postgres

# You'll be prompted for the password you set during installation
```

### macOS/Linux

```bash
# Connect to PostgreSQL
sudo -u postgres psql
```

### In PostgreSQL Shell

```sql
-- Create the database
CREATE DATABASE nexlink_db;

-- Create a dedicated user (recommended for security)
CREATE USER nexlink_user WITH PASSWORD 'your_secure_password_here';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE nexlink_db TO nexlink_user;

-- Grant schema privileges (PostgreSQL 15+)
\c nexlink_db
GRANT ALL ON SCHEMA public TO nexlink_user;

-- Exit PostgreSQL shell
\q
```

## Step 3: Install PostgreSQL Python Adapter

Activate your virtual environment and install `psycopg2`:

```bash
# Windows
myvenv\Scripts\activate
pip install psycopg2-binary

# macOS/Linux
source myvenv/bin/activate
pip install psycopg2-binary
```

## Step 4: Update Environment Configuration

Edit your `.env` file and update the `DATABASE_URL`:

```env
# Comment out or remove the SQLite configuration
# DATABASE_URL=sqlite:///db.sqlite3

# Add PostgreSQL configuration
DATABASE_URL=postgresql://nexlink_user:your_secure_password_here@localhost:5432/nexlink_db
```

**Connection String Format:**
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

Example:
```
DATABASE_URL=postgresql://nexlink_user:mySecurePass123@localhost:5432/nexlink_db
```

## Step 5: Test Database Connection

Test that Django can connect to PostgreSQL:

```bash
python manage.py check --database default
```

If successful, you should see:
```
System check identified no issues (0 silenced).
```

## Step 6: Run Migrations

Create the database schema in PostgreSQL:

```bash
python manage.py migrate
```

This will create all the necessary tables in your PostgreSQL database.

## Step 7: Migrate Data from SQLite (Optional)

If you have existing data in SQLite that you want to preserve:

### Method 1: Using Django's dumpdata/loaddata

```bash
# 1. Backup current SQLite data
# Temporarily switch back to SQLite in .env
DATABASE_URL=sqlite:///db.sqlite3

# 2. Export data from SQLite
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json

# 3. Switch to PostgreSQL in .env
DATABASE_URL=postgresql://nexlink_user:password@localhost:5432/nexlink_db

# 4. Run migrations (if not already done)
python manage.py migrate

# 5. Load data into PostgreSQL
python manage.py loaddata data_backup.json
```

### Method 2: Manual Data Transfer (for specific models)

If you only need to migrate specific data:

```python
# Create a management command: core/management/commands/migrate_data.py
from django.core.management.base import BaseCommand
from core.models import Link, Click
import sqlite3

class Command(BaseCommand):
    help = 'Migrate data from SQLite to PostgreSQL'

    def handle(self, *args, **options):
        # Connect to SQLite
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Migrate Links
        cursor.execute('SELECT * FROM core_link')
        for row in cursor.fetchall():
            Link.objects.create(
                id=row[0],
                original_url=row[1],
                short_code=row[2],
                # ... map other fields
            )
        
        self.stdout.write(self.style.SUCCESS('Data migrated successfully'))
```

## Step 8: Create Superuser

Create a new superuser for the PostgreSQL database:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin account.

## Step 9: Verify Migration

1. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Test the application:**
   - Visit `http://localhost:8000`
   - Create a new short link
   - Test link redirection
   - Check analytics

3. **Access admin panel:**
   - Visit `http://localhost:8000/admin/`
   - Log in with your superuser credentials
   - Verify all models are accessible

## Step 10: Update Requirements

Add PostgreSQL to your `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Or manually add:
```
psycopg2-binary==2.9.9
```

## Troubleshooting

### Connection Refused Error

**Error:** `could not connect to server: Connection refused`

**Solutions:**
- Verify PostgreSQL is running:
  ```bash
  # Windows
  sc query postgresql-x64-14
  
  # macOS
  brew services list
  
  # Linux
  sudo systemctl status postgresql
  ```
- Check if PostgreSQL is listening on the correct port:
  ```bash
  netstat -an | findstr 5432  # Windows
  lsof -i :5432               # macOS/Linux
  ```

### Authentication Failed

**Error:** `FATAL: password authentication failed for user`

**Solutions:**
- Verify username and password in `.env`
- Reset user password in PostgreSQL:
  ```sql
  ALTER USER nexlink_user WITH PASSWORD 'new_password';
  ```

### Permission Denied

**Error:** `permission denied for schema public`

**Solution:**
```sql
-- Connect to the database
\c nexlink_db

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO nexlink_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nexlink_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nexlink_user;
```

### Database Does Not Exist

**Error:** `FATAL: database "nexlink_db" does not exist`

**Solution:**
```sql
CREATE DATABASE nexlink_db;
```

### psycopg2 Installation Issues (Windows)

If you encounter errors installing `psycopg2-binary`:

```bash
# Try installing build tools first
pip install wheel
pip install psycopg2-binary
```

## PostgreSQL Management

### Using pgAdmin (GUI)

1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Navigate to Databases → nexlink_db
4. You can view tables, run queries, and manage data

### Using psql (Command Line)

```bash
# Connect to database
psql -U nexlink_user -d nexlink_db

# Useful commands
\dt              # List all tables
\d table_name    # Describe table structure
\l               # List all databases
\du              # List all users
\q               # Quit
```

### Common SQL Queries

```sql
-- View all links
SELECT * FROM core_link;

-- Count total links
SELECT COUNT(*) FROM core_link;

-- View recent clicks
SELECT * FROM core_click ORDER BY timestamp DESC LIMIT 10;

-- Database size
SELECT pg_size_pretty(pg_database_size('nexlink_db'));
```

## Backup and Restore

### Backup Database

```bash
# Full database backup
pg_dump -U nexlink_user nexlink_db > backup_$(date +%Y%m%d).sql

# Backup specific tables
pg_dump -U nexlink_user -t core_link -t core_click nexlink_db > links_backup.sql
```

### Restore Database

```bash
# Restore full database
psql -U nexlink_user nexlink_db < backup_20260113.sql

# Restore specific tables
psql -U nexlink_user nexlink_db < links_backup.sql
```

## Performance Optimization

### Create Indexes

```sql
-- Already created by Django, but you can add custom indexes
CREATE INDEX idx_link_short_code ON core_link(short_code);
CREATE INDEX idx_click_timestamp ON core_click(timestamp);
```

### Vacuum and Analyze

```sql
-- Optimize database
VACUUM ANALYZE;
```

## Next Steps

- [ ] Set up regular database backups
- [ ] Configure connection pooling for production (PgBouncer)
- [ ] Monitor database performance
- [ ] Set up database replication for high availability (if needed)

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django PostgreSQL Notes](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

**Need Help?** If you encounter issues not covered here, check the PostgreSQL logs:
- Windows: `C:\Program Files\PostgreSQL\14\data\log\`
- macOS: `/usr/local/var/postgres/`
- Linux: `/var/log/postgresql/`
