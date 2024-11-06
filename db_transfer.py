import os
import sys
import django
from django.core.management import call_command
from django.conf import settings
import shutil
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcshop.settings')
django.setup()

def dump_sqlite_data():
    # Force UTF-8 encoding for stdout and stderr
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    
    # Ensure we're using SQLite
    if 'sqlite3' not in settings.DATABASES['default']['ENGINE']:
        raise Exception("Current database is not SQLite")
    
    print("Starting data dump from SQLite...")
    
    # Backup media files
    media_source = os.path.join(settings.MEDIA_ROOT)
    media_backup = os.path.join(settings.BASE_DIR, 'media_backup')
    
    if os.path.exists(media_source):
        if os.path.exists(media_backup):
            shutil.rmtree(media_backup)
        shutil.copytree(media_source, media_backup)
        print("Media files backed up successfully")

    # Create JSON dump with proper encoding
    try:
        print("Creating database dump...")
        
        # Method 1: Using temporary file with UTF-8 encoding
        with open('db_dump.json', 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                exclude=['contenttypes', 'auth.permission'],
                natural_foreign=True,
                natural_primary=True,
                stdout=f,
                indent=2
            )
        
        # Verify the JSON file is properly encoded
        with open('db_dump.json', 'r', encoding='utf-8') as f:
            json.load(f)  # This will raise an exception if JSON is invalid
        
        print("Data dump completed successfully")
        print("\nNow you can:")
        print("1. Change your database settings to PostgreSQL")
        print("2. Run migrate command")
        print("3. Run the load_postgres_data.py script")
        
    except Exception as e:
        print(f"Error occurred during dump: {e}")
        if os.path.exists('db_dump.json'):
            os.remove('db_dump.json')
        
        # Method 2 (Alternative): If Method 1 fails, try direct output
        try:
            print("Trying alternative dump method...")
            with open('db_dump.json', 'w', encoding='utf-8') as f:
                django_data = call_command(
                    'dumpdata',
                    exclude=['contenttypes', 'auth.permission'],
                    natural_foreign=True,
                    natural_primary=True,
                    indent=2
                )
                json.dump(django_data, f, ensure_ascii=False, indent=2)
            print("Alternative dump method succeeded")
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")

if __name__ == '__main__':
    dump_sqlite_data()