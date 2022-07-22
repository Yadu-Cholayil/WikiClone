from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("addentry", views.addentry, name="addentry"),
    path("random", views.RandomPage, name='RandomPage'),
    path('search', views.SearchPage, name='search'),
    path('edit/<str:title>/', views.EditPage, name="Edit")
]
