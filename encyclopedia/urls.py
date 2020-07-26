from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entrypage, name="entrypage"),
    path("templates/encyclopedia/search.html", views.searchentry, name="searchpage"),
    path("templates/encyclopedia/addentry.html", views.addentry, name="addentrypage"),
    path("wiki2/<str:title>", views.editentry, name="editentrypage"),
    path("wiki2/<str:title>", views.editentry, name="editentrypage2"),
    path("randompage/", views.randompage, name="randompage")
]
