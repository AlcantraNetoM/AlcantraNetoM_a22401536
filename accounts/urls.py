from django.urls import path

from . import views

urlpatterns = [
    path("registar/", views.register_view, name="accounts-register"),
    path("login/", views.login_view, name="accounts-login"),
    path("logout/", views.logout_view, name="accounts-logout"),
    path("magic/<str:uidb64>/<str:token>/", views.magic_link_login_view, name="accounts-magic-link"),
]
