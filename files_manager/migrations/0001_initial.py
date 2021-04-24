import django.core.files.storage
from django.db import migrations, models
import django.utils.timezone
import files_manager.models
import pathlib


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('file_hash', models.CharField(default='', max_length=64, primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=255, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media_data/', location=pathlib.PurePosixPath('/home/thinkpad/PythonProjects/file_storage/store')), upload_to=files_manager.models.submit_file_path, validators=[files_manager.models.validate_file])),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Files',
                'ordering': ('-date_created',),
            },
        ),
    ]
