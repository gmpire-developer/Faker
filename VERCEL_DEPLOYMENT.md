# 🚀 Vercel Deployment Guide

## Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- GitHub account with your project repository
- Git installed locally

## Step 1: Prepare Your Repository

1. **Remove local database**
   ```bash
   rm db.sqlite3
   ```

2. **Create `.gitignore` (if not exists)**
   ```
   *.pyc
   __pycache__/
   *.pyo
   *.pyd
   .Python
   env/
   venv/
   .venv
   db.sqlite3
   .env
   .env.local
   node_modules/
   staticfiles/
   .vercel
   ```

3. **Commit and push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

## Step 2: Deploy on Vercel

### Option A: Via Vercel Dashboard (Recommended)

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New"** → **"Project"**
3. **Import Git Repository**
   - Select your GitHub repository
   - Click **"Import"**

4. **Configure Project**
   - **Framework Preset**: None (Django)
   - **Root Directory**: `.` (current directory)
   - **Build Command**: `pip install -r requirements.txt && npm install && npm run build`
   - **Output Directory**: Leave empty
   - **Install Command**: Leave empty

5. **Environment Variables** (click "Add")
   ```
   SECRET_KEY = <generate-random-key>
   DEBUG = False
   ALLOWED_HOSTS = yourdomain.vercel.app
   ```

6. Click **"Deploy"** and wait for deployment to complete

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy project
vercel

# Set environment variables
vercel env add SECRET_KEY
vercel env add DEBUG
vercel env add ALLOWED_HOSTS
```

## Step 3: Generate Secret Key

Create a strong secret key for production:

```python
# In Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and set it as `SECRET_KEY` environment variable in Vercel dashboard.

## Step 4: Set Environment Variables in Vercel

1. Go to **Project Settings** → **Environment Variables**
2. Add these variables:
   - `SECRET_KEY`: Your generated secret key
   - `DEBUG`: `False` (production)
   - `ALLOWED_HOSTS`: `yourdomain.vercel.app,localhost`

3. Redeploy:
   ```bash
   vercel --prod
   ```

## Step 5: Verify Deployment

Visit your Vercel domain (e.g., `yourdomain.vercel.app`) and test:
- ✅ Home page loads
- ✅ Generate page accessible
- ✅ PDF generation works
- ✅ Styling looks correct
- ✅ Mobile responsive

## Troubleshooting

### 1. **Static Files Not Loading**
- Ensure Tailwind CSS is built (`npm run build`)
- Check `STATIC_ROOT` and `STATICFILES_DIRS` in settings
- WhiteNoise middleware will handle static file serving

### 2. **PDF Generation Fails**
- Check that all required fonts are in `static/fonts/`
- Verify PIL/Pillow is installed
- Check logs in Vercel dashboard

### 3. **Transliteration Not Working**
- Ensure Google API is accessible (may be blocked in some regions)
- Fallback transliteration should work offline
- Check browser console for errors

### 4. **Database Issues**
- SQLite is not recommended for production
- For production, use PostgreSQL:
  1. Create PostgreSQL database (use Vercel Postgres or external service)
  2. Add `DATABASE_URL` environment variable
  3. Update `settings.py` to use PostgreSQL

### 5. **Build Failures**
- Check build logs in Vercel dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

## Optimizations for Production

### Use PostgreSQL Instead of SQLite
```python
# config/settings.py
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

### Enable HTTPS Redirect
```python
# config/settings.py
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
```

### Set Security Headers
```python
# config/settings.py
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
```

### Compress CSS/JS
WhiteNoise is already configured for compression in `settings.py`.

## Automatic Deployments

After initial setup:
1. All pushes to `main` branch automatically deploy
2. Pull requests create preview deployments
3. Check deployment status at `vercel.com/dashboard`

## Monitoring

Monitor your application:
1. **Vercel Dashboard**: Deployment status, errors
2. **Build Logs**: Check for build issues
3. **Runtime Logs**: Monitor PDF generation and API calls
4. **Analytics**: Track visitor patterns

## Custom Domain

1. In Vercel dashboard, go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records (Vercel provides instructions)
4. Update `ALLOWED_HOSTS` environment variable

## Important Security Notes

⚠️ **DO NOT**:
- Commit `.env` files with secrets
- Use `DEBUG = True` in production
- Share your `SECRET_KEY`
- Push `db.sqlite3` to production

✅ **DO**:
- Use environment variables for secrets
- Generate strong random `SECRET_KEY`
- Use PostgreSQL for production data
- Enable HTTPS (automatic on Vercel)
- Keep dependencies updated

## Support & Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Vercel Community](https://github.com/vercel/vercel/discussions)

---

**Happy Deploying! 🎉**
