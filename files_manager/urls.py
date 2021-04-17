from django.urls import path

from .views import *


urlpatterns = [
    path('', show_feed),
    path('<slug:file_hash>/', show_details)
]
