from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CompetenciaForm, FormacaoForm, ProjetoForm, TecnologiaForm
from .models import Competencia, Curso, Formacao, MakingOfEntrada, Projeto, Tecnologia, TipoTecnologia, UnidadeCurricular


def cursos_view(request):
	cursos = Curso.objects.prefetch_related("unidades_curriculares").all()
	return render(request, "portfolio/cursos.html", {"cursos": cursos})


def unidades_curriculares_view(request):
	unidades_curriculares = UnidadeCurricular.objects.select_related("curso").all()
	return render(
		request,
		"portfolio/unidades_curriculares.html",
		{"unidades_curriculares": unidades_curriculares},
	)


def sobre_view(request):
	context = {
		"github_repo_url": "https://github.com/AlcantraNetoM/AlcantraNetoM_a22401536",
		"video_url": "https://www.youtube.com/embed/zkaXaIpEdqA",
		"tipos_tecnologia": TipoTecnologia.objects.prefetch_related("tecnologias").all(),
		"making_of_entradas": MakingOfEntrada.objects.all(),
	}
	return render(request, "portfolio/sobre.html", context)


def making_of_view(request):
	entradas = MakingOfEntrada.objects.all()
	return render(request, "portfolio/making_of.html", {"entradas": entradas})


class ProjetoListView(ListView):
	model = Projeto
	template_name = "portfolio/projetos_list.html"
	context_object_name = "projetos"


class ProjetoCreateView(CreateView):
	model = Projeto
	form_class = ProjetoForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-projetos")


class ProjetoUpdateView(UpdateView):
	model = Projeto
	form_class = ProjetoForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-projetos")


class ProjetoDeleteView(DeleteView):
	model = Projeto
	template_name = "portfolio/confirm_delete.html"
	success_url = reverse_lazy("portfolio-projetos")


class TecnologiaListView(ListView):
	model = Tecnologia
	template_name = "portfolio/tecnologias_list.html"
	context_object_name = "tecnologias"

	def get_queryset(self):
		return Tecnologia.objects.select_related("tipo").all()


class TecnologiaCreateView(CreateView):
	model = Tecnologia
	form_class = TecnologiaForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-tecnologias")


class TecnologiaUpdateView(UpdateView):
	model = Tecnologia
	form_class = TecnologiaForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-tecnologias")


class TecnologiaDeleteView(DeleteView):
	model = Tecnologia
	template_name = "portfolio/confirm_delete.html"
	success_url = reverse_lazy("portfolio-tecnologias")


class CompetenciaListView(ListView):
	model = Competencia
	template_name = "portfolio/competencias_list.html"
	context_object_name = "competencias"


class CompetenciaCreateView(CreateView):
	model = Competencia
	form_class = CompetenciaForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-competencias")


class CompetenciaUpdateView(UpdateView):
	model = Competencia
	form_class = CompetenciaForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-competencias")


class CompetenciaDeleteView(DeleteView):
	model = Competencia
	template_name = "portfolio/confirm_delete.html"
	success_url = reverse_lazy("portfolio-competencias")


class FormacaoListView(ListView):
	model = Formacao
	template_name = "portfolio/formacoes_list.html"
	context_object_name = "formacoes"


class FormacaoCreateView(CreateView):
	model = Formacao
	form_class = FormacaoForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-formacoes")


class FormacaoUpdateView(UpdateView):
	model = Formacao
	form_class = FormacaoForm
	template_name = "portfolio/form.html"
	success_url = reverse_lazy("portfolio-formacoes")


class FormacaoDeleteView(DeleteView):
	model = Formacao
	template_name = "portfolio/confirm_delete.html"
	success_url = reverse_lazy("portfolio-formacoes")
