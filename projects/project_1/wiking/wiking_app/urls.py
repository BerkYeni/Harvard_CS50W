from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("search", views.search, name="search"),
  path("new_entry", views.new_entry, name="new_entry"),
  path("no_such_entry/", views.no_such_entry, name="no_such_entry"),
  path("entry_added/", views.entry_added, name="entry_added"),
  path("random_redirect/", views.random_redirect, name="random_redirect"),
  path("entry_add_failed/", views.entry_add_failed, name="entry_add_failed"),
  path("<entry_title>/", views.entry, name="entry"),
  path("<entry_title>/edit_entry/", views.edit_entry, name="edit_entry"),
]