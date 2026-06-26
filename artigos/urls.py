from django.urls import path

from . import views

urlpatterns = [
    path("", views.artigo_list_view, name="artigos-list"),
    path("novo/", views.ArtigoCreateView.as_view(), name="artigos-create"),
    path("<int:pk>/", views.artigo_detail_view, name="artigos-detail"),
    path("<int:pk>/editar/", views.ArtigoUpdateView.as_view(), name="artigos-update"),
    path("<int:pk>/apagar/", views.ArtigoDeleteView.as_view(), name="artigos-delete"),
    path("<int:pk>/comentar/", views.comentar_artigo_view, name="artigos-comment"),
    path("<int:pk>/like/", views.like_artigo_view, name="artigos-like"),
]
