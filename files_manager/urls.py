from django.urls import path

from .views import *


urlpatterns = [
    path('', show_feed, name='files_manager-files_list'),
    path('file_details/<slug:file_hash>/', show_details, name='files_manager-file_details'),
    path('uploading/', upload_file, name='files_manager-uploading_file'),
    path('successful_uploading/', confirm_uploading, name='successful uploading'),
    path('successful_deletion/', confirm_deletion, name='successful deletion')
]
