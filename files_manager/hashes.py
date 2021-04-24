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
    # Returns True if the uploaded file is big enough to require reading in multiple chunks.
    # By default this will be any file larger than 2.5 megabytes, but that’s configurable;
    if not file.multiple_chunks():
        file_hash.update(file.read())
    else:
        for chunk in file.chunks():
            file_hash.update(chunk)

    return file_hash.hexdigest()
