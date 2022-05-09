from django.contrib import admin
from django.urls import path

from . import views

# app urls down here
app_name = "homepage"
urlpatterns = [
    path("", views.index, name="index"),
]
