from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .hashes import calculate_file_hash


def submit_file_path(instance, filename):
    file_hash = instance.file_hash
    sub_dir_name = file_hash[:2]
    return Path(sub_dir_name) / Path(file_hash)


def validate_file(uploading_file):
    # TODO a file is not on a disk, it is in memory, what will happen if file will be larger than capacity of memory?
    file_hash = calculate_file_hash(uploading_file)
    if Data.objects.filter(file_hash=file_hash).exists():
        raise ValidationError(f'The file with this hash is already exists {file_hash}')
    else:
        validate_file.previous_file_hash = file_hash


class Data(models.Model):
    file_hash = models.CharField(primary_key=True, max_length=64, default='')
    file = models.FileField(upload_to=submit_file_path, null=True, validators=[validate_file], max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = '-date_created',
        verbose_name_plural = 'Files'

    def __str__(self):
        return str(self.file.name)


@receiver(signal=pre_save, sender=Data)
def assign_pk(instance, **kwargs):
    instance.file_hash = validate_file.previous_file_hash
