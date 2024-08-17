from django.urls import path

from . import views

app_name = "english"

urlpatterns = [
    path('', views.Index_View.as_view())
]