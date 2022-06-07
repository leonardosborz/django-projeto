from django.urls import include, path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name="register"),
]