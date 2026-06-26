from django.contrib import admin

from .models import Curso, UnidadeCurricular


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
	list_display = ("codigo", "nome", "grau", "ects", "estado_acreditacao")
	ordering = ("nome",)
	search_fields = ("nome", "codigo", "grau", "area_cientifica")
	list_filter = ("grau", "estado_acreditacao", "area_cientifica")


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
	list_display = ("codigo_legivel", "nome", "curso", "ano", "semestre", "ects")
	ordering = ("curso", "ano", "semestre", "nome")
	search_fields = ("nome", "codigo_legivel", "curso__nome")
	list_filter = ("curso", "ano", "semestre", "opcao", "tipo", "natureza")
