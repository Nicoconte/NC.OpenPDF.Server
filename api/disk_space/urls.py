from django.urls import path

from .views import *

urlpatterns = [
    path('info/', get_disk_space),
]
