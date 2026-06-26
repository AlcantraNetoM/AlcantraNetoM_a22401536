from django.shortcuts import render

from .models import Curso, UnidadeCurricular


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
