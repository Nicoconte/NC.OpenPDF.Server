from django.urls import path

from .views import *

urlpatterns = [
    path('merge/', merge_pdf),
    path('encrypt/', encrypt_pdf),
    path('img-to-pdf/', convert_img_to_pdf)
]
