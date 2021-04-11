from hashlib import sha256

from django.db.models.fields.files import FieldFile


def calculate_file_hash(file: FieldFile) -> str:
    file_hash = sha256()
    current_file = file.open()
    file_buffer = current_file.read(file.DEFAULT_CHUNK_SIZE)

    while len(file_buffer) > 0:
        file_hash.update(file_buffer)
        file_buffer = current_file.read(file.DEFAULT_CHUNK_SIZE)

    return file_hash.hexdigest()
