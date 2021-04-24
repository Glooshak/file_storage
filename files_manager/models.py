from pathlib import Path
import logging
from logging import getLogger

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import reverse


from .hashes import calculate_file_hash
from .custom_storage_system import storage
from .utils import obtain_relative_file_path


logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def submit_file_path(instance, filename):
    file_hash = instance.file_hash
    return obtain_relative_file_path(file_hash)


def validate_file(uploading_file):
    file_hash = calculate_file_hash(uploading_file)
    if Data.objects.filter(file_hash=file_hash).exists() and storage.exists(obtain_relative_file_path(file_hash)):
        raise ValidationError(f'The file with this hash is already exists: {file_hash}')
    else:
        validate_file.previous_file_hash = file_hash


class Data(models.Model):
    file_hash = models.CharField(primary_key=True, max_length=64, default='')
    file = models.FileField(
        storage=storage,
        upload_to=submit_file_path,
        null=True,
        validators=[validate_file],
        max_length=255
    )
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = '-date_created',
        verbose_name_plural = 'Files'

    def get_absolute_url(self):
        return reverse('files_manager-file_details', kwargs={'file_hash': self.file_hash})

    def __str__(self):
        return str(self.file_hash)


@receiver(signal=pre_save, sender=Data)
def assign_pk(instance, **kwargs):
    if not instance.file_hash: instance.file_hash = validate_file.previous_file_hash
