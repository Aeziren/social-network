
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.user, name="user"),
    path("following", views.following, name="following"),

    # API routes
    path("follow_toggle", views.follow_toggle, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like")
]
