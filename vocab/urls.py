from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("counts/", views.get_word_counts, name="word-counts"),
    path("find/", views.find_word, name="find-word"),
    path("lemma/", views.get_lemma, name="get-lemma"),
    path("pos/", views.get_pos, name="get-pos"),
    path("valid_pos/", views.check_pos, name="check-pos"),
    path("all_pos/", views.get_all_pos, name="get-all-pos"),
]
