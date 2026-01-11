# ✅ Pre-Deployment Checklist

## Before Pushing to GitHub

- [ ] Remove `db.sqlite3` file
  ```bash
  rm db.sqlite3
  ```

- [ ] Verify `.gitignore` includes:
  - `db.sqlite3`
  - `*.pyc`
  - `__pycache__/`
  - `venv/`
  - `.env`
  - `node_modules/`
  - `staticfiles/`

- [ ] Test build locally
  ```bash
  pip install -r requirements.txt
  npm install && npm run build
  python manage.py collectstatic --noinput
  ```

- [ ] Verify all dependencies in `requirements.txt`

- [ ] Review `.env.example` for required variables

## On Vercel Dashboard

- [ ] Set `SECRET_KEY` environment variable
  - Generate via: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

- [ ] Set `DEBUG = False`

- [ ] Set `ALLOWED_HOSTS` to your domain
  - Format: `yourdomain.vercel.app,localhost`

- [ ] Verify build command runs without errors

## After Deployment

- [ ] Visit your Vercel domain
- [ ] Test home page loads
- [ ] Test generate form
- [ ] Test PDF generation
- [ ] Check console for errors (F12)
- [ ] Test on mobile devices
- [ ] Verify static files load (CSS, images)

## Production Optimization (Optional)

- [ ] Switch to PostgreSQL database
- [ ] Enable HTTPS redirect
- [ ] Set security headers
- [ ] Add custom domain
- [ ] Set up monitoring/logging
- [ ] Test all features thoroughly

## Troubleshooting

If something fails:
1. Check **Vercel Dashboard** → **Deployments** → **Build Logs**
2. Check **Logs** tab for runtime errors
3. Look for specific error messages
4. Common issues:
   - Missing fonts in static/fonts/
   - Incorrect ALLOWED_HOSTS
   - Missing environment variables
   - Static files not collected

## Roll Back

To revert to a previous deployment:
1. Go to **Vercel Dashboard** → **Deployments**
2. Find the working deployment
3. Click the three dots → **Promote to Production**

---

**Once all checks pass, you're ready for production! 🚀**
