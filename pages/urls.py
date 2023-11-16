from django.urls import path
from .views import *


urlpatterns = [
    path("", tariffs_page_view),
    path("tariff/", tariff_page_view),
    path("success/", success_page_view),
]
