"""
Vercel build script for Django project.
Runs during deployment to prepare static files.
"""
import os
import subprocess
import sys

print("=" * 60)
print("VERCEL BUILD STARTED")
print("=" * 60)

# Install Tailwind dependencies and build CSS
print("\n[1/3] Installing npm dependencies...")
result = subprocess.run(["npm", "install"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
    sys.exit(1)

print("\n[2/3] Building Tailwind CSS...")
result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
    sys.exit(1)

# Verify CSS file was created
css_file = "static/css/style.css"
if os.path.exists(css_file):
    size = os.path.getsize(css_file)
    print(f"✓ CSS file created: {css_file} ({size} bytes)")
else:
    print(f"✗ ERROR: CSS file not found at {css_file}")
    sys.exit(1)

print("\n[3/3] Collecting static files...")
result = subprocess.run(["python", "manage.py", "collectstatic", "--noinput", "--clear"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
    sys.exit(1)

print("\n" + "=" * 60)
print("BUILD COMPLETED SUCCESSFULLY!")
print("=" * 60)

