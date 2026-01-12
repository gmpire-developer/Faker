"""
Vercel build script for Django project.
Runs during deployment to prepare static files.
"""
import os
import subprocess

# Install Tailwind dependencies and build CSS
print("Installing npm dependencies...")
subprocess.run(["npm", "install"], check=True)

print("Building Tailwind CSS...")
subprocess.run(["npm", "run", "build"], check=True)

print("Collecting static files...")
subprocess.run(["python", "manage.py", "collectstatic", "--noinput"], check=True)

print("Build completed successfully!")
