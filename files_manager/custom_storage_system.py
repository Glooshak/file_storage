from pathlib import Path

from django.core.files.storage import FileSystemStorage
from storage.settings import BASE_DIR


storage_path = BASE_DIR / Path('store')
base_url = '/media_data/'

storage = FileSystemStorage(location=storage_path, base_url=base_url)
