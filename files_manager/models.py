from pathlib import Path

from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .hashes import calculate_file_hash


def submit_file_path(instance, filename):
    file_hash = calculate_file_hash(instance.file)
    sub_dir_name = file_hash[:2]
    return Path(sub_dir_name) / Path(file_hash)


class Data(models.Model):
    # TODO If there is a file with the already existed hash UNIQUE constraint failed will raise
    # TODO need to handle this issue.
    file_hash = models.CharField(primary_key=True, max_length=64, default='')
    file = models.FileField(upload_to=submit_file_path, null=True, max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = '-date_created',
        verbose_name_plural = 'Files'

    def __str__(self):
        return str(self.file.name)


@receiver(signal=pre_save, sender=Data)
def assign_pk(instance, **kwargs):
    instance.file_hash = calculate_file_hash(instance.file)
