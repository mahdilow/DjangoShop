import os
import django
from django.core.management import call_command
from django.conf import settings
import shutil

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcshop.settings')
django.setup()

def load_postgres_data():
    # Ensure we're using PostgreSQL
    if 'postgresql' not in settings.DATABASES['default']['ENGINE']:
        raise Exception("Current database is not PostgreSQL")
    
    print("Starting data load to PostgreSQL...")
    
    try:
        # Check if dump file exists
        if not os.path.exists('db_dump.json'):
            raise Exception("db_dump.json not found")
        
        # Load data from JSON dump
        print("Loading data into PostgreSQL...")
        call_command('loaddata', 'db_dump.json')
        
        # Restore media files if backup exists
        media_backup = os.path.join(settings.BASE_DIR, 'media_backup')
        if os.path.exists(media_backup):
            media_destination = os.path.join(settings.MEDIA_ROOT)
            if os.path.exists(media_destination):
                shutil.rmtree(media_destination)
            shutil.copytree(media_backup, media_destination)
            print("Media files restored successfully")
        
        print("Data load completed successfully")
        
        # Cleanup
        os.remove('db_dump.json')
        if os.path.exists(media_backup):
            shutil.rmtree(media_backup)
            
    except Exception as e:
        print(f"Error occurred during load: {e}")

if __name__ == '__main__':
    load_postgres_data()