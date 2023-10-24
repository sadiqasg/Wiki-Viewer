from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("error/", views.error, name="error_page"),
    path("wiki/<str:wiki_title>", views.wiki_entry, name="wiki_entry"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/new/", views.new, name="new"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random, name="random")
]