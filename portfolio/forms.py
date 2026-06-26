from django import forms

from .models import Competencia, Formacao, MakingOfEntrada, Projeto, Tecnologia, TipoTecnologia


class TipoTecnologiaForm(forms.ModelForm):
	class Meta:
		model = TipoTecnologia
		fields = ["nome", "descricao"]
		widgets = {
			"descricao": forms.Textarea(attrs={"rows": 4}),
		}


class TecnologiaForm(forms.ModelForm):
	class Meta:
		model = Tecnologia
		fields = ["nome", "tipo", "descricao", "vantagens", "desvantagens", "url"]
		widgets = {
			"descricao": forms.Textarea(attrs={"rows": 4}),
			"vantagens": forms.Textarea(attrs={"rows": 4}),
			"desvantagens": forms.Textarea(attrs={"rows": 4}),
		}


class CompetenciaForm(forms.ModelForm):
	class Meta:
		model = Competencia
		fields = ["nome", "descricao"]
		widgets = {
			"descricao": forms.Textarea(attrs={"rows": 4}),
		}


class FormacaoForm(forms.ModelForm):
	class Meta:
		model = Formacao
		fields = ["nome", "instituicao", "descricao", "ano_inicio", "ano_fim", "url"]
		widgets = {
			"descricao": forms.Textarea(attrs={"rows": 4}),
		}


class ProjetoForm(forms.ModelForm):
	class Meta:
		model = Projeto
		exclude = ["data_criacao"]
		widgets = {
			"descricao": forms.Textarea(attrs={"rows": 4}),
			"resumo": forms.Textarea(attrs={"rows": 3}),
		}


class MakingOfEntradaForm(forms.ModelForm):
	class Meta:
		model = MakingOfEntrada
		fields = ["data", "commit_hash", "iteracao", "titulo", "descricao", "alteracoes", "dificuldades", "resultado"]
		widgets = {
			"data": forms.DateInput(attrs={"type": "date"}),
			"descricao": forms.Textarea(attrs={"rows": 4}),
			"alteracoes": forms.Textarea(attrs={"rows": 4}),
			"dificuldades": forms.Textarea(attrs={"rows": 4}),
			"resultado": forms.Textarea(attrs={"rows": 4}),
		}