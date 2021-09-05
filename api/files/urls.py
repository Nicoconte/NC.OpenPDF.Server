from django.urls import path

from .views import *

urlpatterns = [
    path('upload/', upload_file),
    path('all/', list_files),
    path('download/<int:id>/', download_file),
    path('remove/<int:id>/', delete_file),
    path('remove/all/', remove_every_file)
]
