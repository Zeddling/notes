from django.urls import path
from notes import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<slug:category_name_slug>", views.show_category, name="category"),
    path("add-category", views.add_category, name="add_category"),
    path("note/<slug:category_name_slug>", views.add_notes, name="add_note"),
    path("note/<slug:category_name_slug>/<uuid:id>", views.show_note, name="note"),
]
