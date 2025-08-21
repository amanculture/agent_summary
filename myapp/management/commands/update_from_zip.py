import requests
import zipfile
import io
import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from decouple import config

ZIP_URL = config('ZIP_URL')
USERNAME = config('USERNAME')
APP_PASSWORD = config('APP_PASSWORD')



PROJECT_PATH = settings.BASE_DIR 

EXCLUDE_FILES = {".env", "web.config", "db.sqlite3", "settings.py"}
EXCLUDE_FOLDERS = {"media", "staticfiles", "venv", ".venv", "__pycache__", "update_tmp"}

class Command(BaseCommand):
    help = "Update project from Bitbucket ZIP"

    def handle(self, *args, **kwargs):
        extract_path = os.path.join(PROJECT_PATH, "update_tmp")

        try:
            # ✅ Authenticate and download ZIP
            self.stdout.write("📥 Downloading project from Bitbucket...")
            r = requests.get(ZIP_URL, auth=(USERNAME, APP_PASSWORD))
            r.raise_for_status()

            # ✅ Extract ZIP
            z = zipfile.ZipFile(io.BytesIO(r.content))

            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)

            z.extractall(extract_path)

            # Find the root folder inside the ZIP (e.g. repo-name-main)
            inner_folder = os.path.join(extract_path, os.listdir(extract_path)[0])

            self.stdout.write(f"📂 Extracted into {inner_folder}")

            # ✅ Walk through extracted files
            for root, dirs, files in os.walk(inner_folder):
                # Exclude unwanted directories
                dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]

                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), inner_folder)

                    # Skip excluded files
                    if file in EXCLUDE_FILES:
                        self.stdout.write(f"⏭ Skipped file: {rel_path}")
                        continue

                    # Destination path
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(PROJECT_PATH, rel_path)

                    # Ensure destination directory exists
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                    # Copy file
                    shutil.copy2(src_file, dest_file)
                    self.stdout.write(f"✅ Updated: {rel_path}")

            # ✅ Cleanup
            shutil.rmtree(extract_path, ignore_errors=True)
            self.stdout.write(self.style.SUCCESS("🚀 Project successfully updated from Bitbucket!"))

        except Exception as e:
            # Cleanup if error occurs
            if os.path.exists(extract_path):
                shutil.rmtree(extract_path, ignore_errors=True)
            raise CommandError(f"❌ Update failed: {e}")