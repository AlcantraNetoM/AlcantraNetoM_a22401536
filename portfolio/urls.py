from django.urls import path

from . import views

urlpatterns = [
    path("", views.sobre_view, name="portfolio-home"),
    path("sobre/", views.sobre_view, name="portfolio-sobre"),
    path("cursos/", views.cursos_view, name="portfolio-cursos"),
    path("unidades-curriculares/", views.unidades_curriculares_view, name="portfolio-unidades-curriculares"),
    path("making-of/", views.making_of_view, name="portfolio-making-of"),
    path("projetos/", views.ProjetoListView.as_view(), name="portfolio-projetos"),
    path("projetos/novo/", views.ProjetoCreateView.as_view(), name="portfolio-projeto-novo"),
    path("projetos/<int:pk>/editar/", views.ProjetoUpdateView.as_view(), name="portfolio-projeto-editar"),
    path("projetos/<int:pk>/apagar/", views.ProjetoDeleteView.as_view(), name="portfolio-projeto-apagar"),
    path("tecnologias/", views.TecnologiaListView.as_view(), name="portfolio-tecnologias"),
    path("tecnologias/nova/", views.TecnologiaCreateView.as_view(), name="portfolio-tecnologia-nova"),
    path("tecnologias/<int:pk>/editar/", views.TecnologiaUpdateView.as_view(), name="portfolio-tecnologia-editar"),
    path("tecnologias/<int:pk>/apagar/", views.TecnologiaDeleteView.as_view(), name="portfolio-tecnologia-apagar"),
    path("competencias/", views.CompetenciaListView.as_view(), name="portfolio-competencias"),
    path("competencias/nova/", views.CompetenciaCreateView.as_view(), name="portfolio-competencia-nova"),
    path("competencias/<int:pk>/editar/", views.CompetenciaUpdateView.as_view(), name="portfolio-competencia-editar"),
    path("competencias/<int:pk>/apagar/", views.CompetenciaDeleteView.as_view(), name="portfolio-competencia-apagar"),
    path("formacoes/", views.FormacaoListView.as_view(), name="portfolio-formacoes"),
    path("formacoes/nova/", views.FormacaoCreateView.as_view(), name="portfolio-formacao-nova"),
    path("formacoes/<int:pk>/editar/", views.FormacaoUpdateView.as_view(), name="portfolio-formacao-editar"),
    path("formacoes/<int:pk>/apagar/", views.FormacaoDeleteView.as_view(), name="portfolio-formacao-apagar"),
]
