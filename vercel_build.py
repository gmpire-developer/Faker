"""
Vercel build script - Entry point for build
"""
import os
import subprocess
import sys
import shutil

print("=" * 60)
print("VERCEL BUILD - Installing dependencies and building CSS")
print("=" * 60)

# Clean previous builds
if os.path.exists("staticfiles"):
    shutil.rmtree("staticfiles")
    print("✓ Cleaned previous staticfiles")

# Install npm dependencies
print("\n[1/3] Installing npm dependencies...")
subprocess.run(["npm", "install"], check=True)
print("✓ npm dependencies installed")

# Build Tailwind CSS
print("\n[2/3] Building Tailwind CSS...")
subprocess.run(["npm", "run", "build"], check=True)

# Verify CSS file
css_file = "static/css/style.css"
if os.path.exists(css_file):
    size = os.path.getsize(css_file)
    print(f"✓ CSS built: {css_file} ({size:,} bytes)")
else:
    print(f"✗ ERROR: CSS file not found")
    sys.exit(1)

# Collect static files
print("\n[3/3] Collecting static files...")
subprocess.run(["python", "manage.py", "collectstatic", "--noinput", "--clear"], check=True)

# Verify staticfiles directory
if os.path.exists("staticfiles/css/style.css"):
    size = os.path.getsize("staticfiles/css/style.css")
    print(f"✓ Static files collected: staticfiles/css/style.css ({size:,} bytes)")
else:
    print("✗ ERROR: CSS not found in staticfiles")
    sys.exit(1)

print("\n" + "=" * 60)
print("BUILD COMPLETED SUCCESSFULLY")
print("=" * 60)


