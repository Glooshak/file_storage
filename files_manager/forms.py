from django import forms
from django.core.exceptions import ValidationError

from .models import Data
from .hashes import calculate_file_hash


class FileUploadForm(forms.Form):
    file = forms.FileField()
    file_hash = None

    def save_file(self):
        instance = Data(file_hash=self.file_hash, file=self.cleaned_data['file'])
        instance.save()

    # Django agreement clean_(field) to validate the field
    def clean_file(self):
        file = self.cleaned_data['file']
        self.file_hash = calculate_file_hash(file)
        if Data.objects.filter(file_hash=self.file_hash).count():
            ValidationError(f'File with hash {file_hash} is already exists!')
        return file
