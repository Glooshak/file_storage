from pathlib import Path

from django.db import models
from django.utils import timezone
from django.conf.global_settings import MEDIA_URL

from .hashes import calculate_file_hash


def submit_file_path(instance, filename):
    file_hash = calculate_file_hash(instance.file)
    sub_dir_name = file_hash[:2]
    return Path(sub_dir_name) / Path(file_hash)


class Data(models.Model):
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=submit_file_path, null=True, max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = '-date_created',
        verbose_name_plural = 'Files'

    def __str__(self):
        return str(self.file.name)
