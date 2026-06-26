from django.urls import path

from . import views

urlpatterns = [
    path("", views.cursos_view, name="portfolio-home"),
    path("cursos/", views.cursos_view, name="portfolio-cursos"),
    path("unidades-curriculares/", views.unidades_curriculares_view, name="portfolio-unidades-curriculares"),
]
