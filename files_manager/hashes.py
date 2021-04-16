from hashlib import sha256

from django.db.models.fields.files import FieldFile


def calculate_file_hash(file: FieldFile) -> str:
    # Together the MemoryFileUploadHandler and TemporaryFileUploadHandler
    # provide Django’s default file upload behavior of reading small files
    # into memory and large ones onto disk.
    # If a file is large file will be an instance of TemporaryUploadedFile,
    # TemporaryUploadedFile.temporary_file_path() returns the full path to the temporary uploaded file.
    # If a file is small file will be an instance of InMemoryUploadedFile.
    file_hash = sha256()
    file_buffer = file.read(file.DEFAULT_CHUNK_SIZE)
    while len(file_buffer) > 0:
        file_hash.update(file_buffer)
        file_buffer = file.read(file.DEFAULT_CHUNK_SIZE)

    return file_hash.hexdigest()
