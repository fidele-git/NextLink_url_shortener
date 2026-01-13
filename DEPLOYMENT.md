# Deployment Guide

This guide covers deploying NexLink to production environments.

## Prerequisites

- PostgreSQL 12+ database
- Python 3.8+
- Redis (recommended for caching)
- Web server (Nginx or Apache)
- SSL certificate (Let's Encrypt recommended)

## PostgreSQL Database Setup

### Local Installation

#### Windows
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Add PostgreSQL to your PATH (usually done automatically)

#### macOS
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Create Database

```bash
# Switch to postgres user (Linux/macOS)
sudo -u postgres psql

# Or connect directly (Windows/if postgres user has password)
psql -U postgres
```

In PostgreSQL shell:
```sql
-- Create database
CREATE DATABASE nexlink_db;

-- Create user (optional, for better security)
CREATE USER nexlink_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nexlink_db TO nexlink_user;

-- Exit
\q
```

### Connection String

Update your `.env` file:
```
# Using postgres superuser
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/nexlink_db

# Or using dedicated user (recommended)
DATABASE_URL=postgresql://nexlink_user:your_secure_password@localhost:5432/nexlink_db
```

## Environment Configuration

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Generate Secret Key

```python
# Run in Python shell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Update .env File

```env
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/nexlink_db
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
```

## Application Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
source myvenv/bin/activate  # macOS/Linux
myvenv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Production Server Setup

### Using Gunicorn (Recommended)

#### 1. Install Gunicorn

```bash
pip install gunicorn
```

#### 2. Create Gunicorn Configuration

Create `gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
```

#### 3. Run Gunicorn

```bash
gunicorn nexlink_project.wsgi:application -c gunicorn_config.py
```

### Using systemd (Linux)

Create `/etc/systemd/system/nexlink.service`:
```ini
[Unit]
Description=NexLink Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/nexlink
Environment="PATH=/path/to/nexlink/myvenv/bin"
ExecStart=/path/to/nexlink/myvenv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          nexlink_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable nexlink
sudo systemctl start nexlink
sudo systemctl status nexlink
```

## Nginx Configuration

Create `/etc/nginx/sites-available/nexlink`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;

    client_max_body_size 10M;

    location /static/ {
        alias /path/to/nexlink/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /path/to/nexlink/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/nexlink /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
```

## Redis Setup (Optional but Recommended)

### Local Installation

#### Ubuntu/Debian
```bash
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

#### macOS
```bash
brew install redis
brew services start redis
```

#### Windows
Download from [redis.io](https://redis.io/download) or use WSL

### Cloud Redis (Upstash)

1. Sign up at [upstash.com](https://upstash.com)
2. Create a Redis database
3. Copy the connection URL to your `.env` file

## Production Checklist

- [ ] PostgreSQL database created and configured
- [ ] Environment variables set in `.env`
- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured with your domain
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Static files collected
- [ ] Gunicorn installed and configured
- [ ] Nginx configured as reverse proxy
- [ ] SSL certificate installed
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] Redis configured (if using)
- [ ] Firewall configured (allow 80, 443)
- [ ] Regular backups scheduled
- [ ] Monitoring set up

## Backup and Maintenance

### Database Backup

```bash
# Backup
pg_dump -U nexlink_user nexlink_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U nexlink_user nexlink_db < backup_20260113.sql
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Activate virtual environment
source myvenv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo systemctl restart nexlink
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check connection string in `.env`
- Ensure database and user exist
- Check PostgreSQL logs: `/var/log/postgresql/`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check Nginx configuration
- Verify file permissions

### 502 Bad Gateway
- Check Gunicorn is running: `sudo systemctl status nexlink`
- Verify bind address in Gunicorn config
- Check application logs

### Permission Errors
```bash
# Fix ownership
sudo chown -R www-data:www-data /path/to/nexlink

# Fix permissions
sudo chmod -R 755 /path/to/nexlink
```

## Monitoring and Logs

### Application Logs
```bash
# Systemd logs
sudo journalctl -u nexlink -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Performance Monitoring
- Set up monitoring with tools like:
  - Sentry (error tracking)
  - New Relic (APM)
  - Prometheus + Grafana (metrics)

## Scaling Considerations

- **Database**: Consider connection pooling with PgBouncer
- **Cache**: Use Redis for session storage and caching
- **Static Files**: Serve from CDN (CloudFlare, AWS CloudFront)
- **Application**: Increase Gunicorn workers based on CPU cores
- **Load Balancing**: Use multiple application servers with load balancer

---

For additional help, consult the [Django deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/).
