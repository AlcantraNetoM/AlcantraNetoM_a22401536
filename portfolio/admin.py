from django.contrib import admin

from .models import (
	Competencia,
	Curso,
	Formacao,
	MakingOfEntrada,
	Projeto,
	Tecnologia,
	TipoTecnologia,
	UnidadeCurricular,
)


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


@admin.register(TipoTecnologia)
class TipoTecnologiaAdmin(admin.ModelAdmin):
	list_display = ("nome",)
	search_fields = ("nome",)


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
	list_display = ("nome", "tipo")
	search_fields = ("nome", "tipo__nome", "descricao")
	list_filter = ("tipo",)


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
	list_display = ("nome",)
	search_fields = ("nome", "descricao")


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
	list_display = ("nome", "instituicao", "ano_inicio", "ano_fim")
	search_fields = ("nome", "instituicao", "descricao")


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
	list_display = ("titulo", "data_criacao")
	search_fields = ("titulo", "resumo", "descricao")
	filter_horizontal = ("tecnologias", "competencias", "formacoes")


@admin.register(MakingOfEntrada)
class MakingOfEntradaAdmin(admin.ModelAdmin):
	list_display = ("data", "iteracao", "titulo", "commit_hash")
	search_fields = ("titulo", "descricao", "commit_hash")
