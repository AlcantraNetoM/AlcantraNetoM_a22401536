from django.urls import path

from .views import alunos_view, curso_view, cursos_view, professores_view

urlpatterns = [
    path("cursos/", cursos_view, name="cursos"),
    path("curso/<int:id>/", curso_view, name="curso"),
    path("professores/", professores_view, name="professores"),
    path("alunos/", alunos_view, name="alunos"),
    path("", cursos_view),
]
