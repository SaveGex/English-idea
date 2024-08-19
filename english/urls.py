from django.urls import path

from . import views

app_name = "English"

urlpatterns = [
    path('page=<int:page_number>/', views.Index_View.as_view(), name = 'common'),
    path('create/', views.Create_View.as_view(), name = 'create'),
    path('execute/<int:id>/', views.Execute_View.as_view(), name = 'execute'),
]