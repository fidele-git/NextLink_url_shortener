# Neon PostgreSQL Setup Guide (Production-Ready)

Follow these steps to set up a production-ready PostgreSQL database using Neon.

## Step 1: Create Neon Account

1. Go to: **https://neon.tech**
2. Click **"Sign Up"** (you can use GitHub, Google, or email)
3. Verify your email if needed

## Step 2: Create a New Project

1. After logging in, click **"Create a project"** or **"New Project"**
2. Configure your project:
   - **Project name**: `nexlink` (or any name you prefer)
   - **Region**: Choose closest to your users (e.g., US East, EU West)
   - **PostgreSQL version**: 16 (latest, recommended)
3. Click **"Create Project"**

## Step 3: Get Your Connection String

After creating the project, you'll see a **Connection Details** page.

### Copy the Connection String

You'll see something like this:

```
postgresql://username:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**IMPORTANT**: Copy this entire connection string! You'll need it in the next step.

### Alternative: Manual Connection Details

If you prefer to see the details separately:
- **Host**: `ep-cool-name-123456.us-east-2.aws.neon.tech`
- **Database**: `neondb`
- **User**: `username`
- **Password**: `your-password`
- **Port**: `5432`

## Step 4: Update Your .env File

1. Open your `.env` file: `c:\Users\HP ELITEBOOK\nexLink\.env`

2. Find the `DATABASE_URL` line and replace it with your Neon connection string:

```env
DATABASE_URL=postgresql://your-username:your-password@ep-your-project.region.aws.neon.tech/neondb?sslmode=require
```

**Example of complete .env file:**
```env
DEBUG=True
SECRET_KEY=django-insecure-nexlink-dev-key-12345
REDIS_URL=rediss://default:your-redis-password@your-redis-host.upstash.io:6379

# Neon PostgreSQL Database
DATABASE_URL=postgresql://your-username:your-password@ep-your-project.region.aws.neon.tech/neondb?sslmode=require

ALLOWED_HOSTS=localhost,127.0.0.1
SECURE_SSL_REDIRECT=False
```

3. Save the file

## Step 5: Run Migrations

Once you've updated the `.env` file, let me know and I'll run:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Step 6: Verify Setup

After migrations complete, test:
- ✅ Application runs without errors
- ✅ Can create short links
- ✅ Links are stored in Neon database
- ✅ Admin panel works

## Benefits of Neon

✅ **Serverless**: Auto-scales based on usage
✅ **Free Tier**: 0.5 GB storage, perfect for starting
✅ **Automatic Backups**: Point-in-time recovery
✅ **Branching**: Create database branches for testing
✅ **Fast**: Low latency worldwide
✅ **Secure**: SSL/TLS encryption by default

## Neon Dashboard Features

In your Neon dashboard, you can:
- View database metrics and usage
- Create database branches for testing
- Manage connection pooling
- Set up automatic backups
- Monitor queries and performance

## Next Steps After Setup

1. **Test locally**: Verify everything works with Neon
2. **Deploy app**: Deploy to Vercel, Railway, or Heroku
3. **Update ALLOWED_HOSTS**: Add your production domain
4. **Set DEBUG=False**: For production
5. **Generate new SECRET_KEY**: For production security

---

## Quick Start Checklist

- [ ] Sign up at https://neon.tech
- [ ] Create new project named "nexlink"
- [ ] Copy the PostgreSQL connection string
- [ ] Update `.env` file with DATABASE_URL
- [ ] Let me know when ready, and I'll run migrations
- [ ] Test the application

---

**Need help?** Just paste your Neon connection string here (I'll help you format it correctly for the `.env` file).

**Security Note**: Never commit your `.env` file to Git. It's already in `.gitignore` for protection.
