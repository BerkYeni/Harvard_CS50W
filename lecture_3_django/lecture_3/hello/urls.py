from django.urls import path
from . import views
urlpatterns = [
  path("", views.index, name="index"),
  path("user", views.user, name="user"),
  path("developer", views.developer, name="developer"),
  path("<str:name>", views.greet, name="greet"),
]