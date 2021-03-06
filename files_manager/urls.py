from django.urls import path

from .views import *


urlpatterns = [
    path('', ShowingFeed.as_view(), name='files_manager-files_list'),
    path('file_details/<slug:file_hash>/', show_details, name='files_manager-file_details'),
    path('uploading/', FileUploadView.as_view(), name='files_manager-uploading_file'),
    path('successful_uploading/', confirm_uploading, name='files_manager-successful_uploading'),
    path('successful_deletion/<slug:file_hash>/', execute_deletion, name='files_manager-successful_deletion'),
    path(
        'successful_downloading/<slug:file_hash>/',
        DownloadingFile.as_view(),
        name='files_manager-successful_downloading'
    ),
    path('search/', Searching.as_view(), name='files_manager-searching')
]
