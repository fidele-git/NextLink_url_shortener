# NexLink - Modern URL Shortener

A powerful, feature-rich URL shortening service built with Django. NexLink provides a clean, modern interface for creating and managing short links with advanced analytics and user management.

## ✨ Features

- **URL Shortening**: Create short, memorable links from long URLs
- **Custom Aliases**: Set custom short codes for your links
- **Analytics Dashboard**: Track clicks, referrers, and user agents
- **QR Code Generation**: Generate QR codes for any shortened link
- **User Authentication**: Secure user accounts with email/password and Google OAuth
- **Link Management**: View, edit, and delete your links
- **Click Tracking**: Detailed analytics for each link
- **Redis Caching**: Fast performance with Redis integration
- **Modern Admin Panel**: Beautiful Unfold admin interface
- **Responsive Design**: Works seamlessly on desktop and mobile

## 🛠️ Technology Stack

- **Backend**: Django 5.x
- **Database**: PostgreSQL (SQLite for development)
- **Cache**: Redis (via Upstash or local)
- **Authentication**: Django Allauth (Email + Google OAuth)
- **Frontend**: HTML, CSS, JavaScript with HTMX
- **Admin**: Django Unfold
- **QR Codes**: qrcode library

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+ (for production)
- Redis (optional, for caching)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nexlink.git
cd nexlink
```

### 2. Create Virtual Environment

```bash
python -m venv myvenv
# On Windows
myvenv\Scripts\activate
# On macOS/Linux
source myvenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
copy .env.example .env  # Windows
# or
cp .env.example .env    # macOS/Linux
```

Edit `.env` and update the following:
- `SECRET_KEY`: Generate a new secret key
- `DATABASE_URL`: Your PostgreSQL connection string
- `REDIS_URL`: Your Redis connection string (if using)

### 5. Set Up PostgreSQL Database

```bash
# Create database
createdb nexlink_db

# Or using psql
psql -U postgres
CREATE DATABASE nexlink_db;
\q
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

## 📖 Usage

### Creating Short Links

1. **Anonymous Users**: Visit the homepage and paste your URL
2. **Registered Users**: Log in to access the dashboard for custom aliases and analytics

### Managing Links

- Access your dashboard at `/dashboard/`
- View all your links with click statistics
- Edit or delete links
- Generate QR codes
- View detailed analytics

### Admin Panel

Access the admin panel at `/admin/` with your superuser credentials to:
- Manage users
- View all links
- Monitor click analytics
- Configure site settings

## 🔧 Configuration

### Database

The application uses `DATABASE_URL` from the `.env` file. Format:

```
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/nexlink_db

# SQLite (development only)
DATABASE_URL=sqlite:///db.sqlite3
```

### Redis Caching

For better performance, configure Redis:

```
REDIS_URL=redis://localhost:6379/0
# Or for Upstash
REDIS_URL=rediss://default:password@host:port
```

### Google OAuth (Optional)

1. Create a project in [Google Cloud Console](https://console.cloud.google.com)
2. Enable Google+ API
3. Create OAuth 2.0 credentials
4. Add credentials to Django admin under "Social applications"

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Generate a strong `SECRET_KEY`
- [ ] Configure PostgreSQL database
- [ ] Set up Redis for caching
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable SSL (`SECURE_SSL_REDIRECT=True`)
- [ ] Collect static files
- [ ] Run migrations
- [ ] Set up a reverse proxy (Nginx/Apache)
- [ ] Configure HTTPS

## 📁 Project Structure

```
nexlink/
├── core/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── utils.py           # Utility functions
├── nexlink_project/       # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not in git)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django framework and community
- Unfold admin theme
- Django Allauth for authentication
- All contributors and users

## 📧 Support

For support, email support@nexlink.com or open an issue on GitHub.

---

Made with ❤️ using Django
