from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("counts/", views.get_word_counts, name="word-counts"),
    path("find/", views.find_word, name="find-word"),
]
