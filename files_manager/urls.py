from django.urls import path

from .views import *


urlpatterns = [
    path('', show_feed, name='files_list'),
    path('file_detail/<slug:file_hash>/', show_details, name='file_detail'),
    path('uploading/', upload_file, name='uploading_file')
]
