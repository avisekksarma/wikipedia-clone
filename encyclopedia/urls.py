from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.topics, name="topics"),
    path("search", views.searchresults, name='search'),
    path("create", views.createpage, name='createpage'),
    path("edit/<str:title>", views.edit, name="edit"),
    path("randompage", views.randompage, name="randompage")
]
