from django.db import models


class Curso(models.Model):
	codigo = models.PositiveIntegerField(unique=True)
	nome = models.CharField(max_length=255)
	grau = models.CharField(max_length=255, blank=True)
	plano_curricular_codigo = models.PositiveIntegerField(null=True, blank=True)
	plano_curricular_nome = models.CharField(max_length=255, blank=True)
	area_cientifica = models.CharField(max_length=255, blank=True)
	codigo_area_cientifica = models.CharField(max_length=50, blank=True)
	cnaef = models.CharField(max_length=50, blank=True)
	ects = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
	estado_acreditacao = models.CharField(max_length=255, blank=True)
	codigo_estado_acreditacao = models.CharField(max_length=50, blank=True)
	data_publicacao = models.DateField(null=True, blank=True)
	apresentacao = models.TextField(blank=True)
	objetivos = models.TextField(blank=True)
	saidas_profissionais = models.TextField(blank=True)
	condicoes_acesso = models.TextField(blank=True)
	estudos_futuros = models.TextField(blank=True)
	contactos_direcao = models.CharField(max_length=255, blank=True)
	email_direcao = models.EmailField(blank=True)
	contactos_secretariado = models.CharField(max_length=255, blank=True)
	email_secretariado = models.EmailField(blank=True)
	url = models.URLField(blank=True)

	class Meta:
		ordering = ("nome",)

	def __str__(self):
		return f"{self.nome} ({self.codigo})"


class UnidadeCurricular(models.Model):
	curso = models.ForeignKey(
		Curso,
		related_name="unidades_curriculares",
		on_delete=models.CASCADE,
	)
	codigo_legivel = models.CharField(max_length=50, unique=True)
	codigo = models.PositiveIntegerField()
	nome = models.CharField(max_length=255)
	ano = models.PositiveSmallIntegerField()
	semestre = models.CharField(max_length=20)
	semestre_codigo = models.CharField(max_length=10)
	ects = models.DecimalField(max_digits=4, decimal_places=1)
	grupo_codigo = models.PositiveSmallIntegerField(null=True, blank=True)
	grupo_nome = models.CharField(max_length=255, blank=True)
	ramo_codigo = models.PositiveSmallIntegerField(null=True, blank=True)
	ramo_nome = models.CharField(max_length=255, blank=True)
	opcao_codigo = models.CharField(max_length=10, blank=True)
	opcao = models.CharField(max_length=100, blank=True)
	horas_contacto = models.PositiveSmallIntegerField(null=True, blank=True)
	horas_contacto_int = models.PositiveSmallIntegerField(null=True, blank=True)
	mobilidade_entrada = models.BooleanField(default=False)
	mobilidade_saida = models.BooleanField(default=False)
	lingua = models.CharField(max_length=20, blank=True)
	lingua_codigo = models.CharField(max_length=20, blank=True)
	tipo = models.CharField(max_length=100, blank=True)
	natureza = models.CharField(max_length=100, blank=True)
	diploma = models.CharField(max_length=255, blank=True)
	apresentacao = models.TextField(blank=True)
	objetivos = models.TextField(blank=True)
	programa = models.TextField(blank=True)
	metodologia = models.TextField(blank=True)
	avaliacao = models.TextField(blank=True)
	bibliografia = models.TextField(blank=True)
	competencias = models.TextField(blank=True)

	class Meta:
		ordering = ("curso", "ano", "semestre", "nome")

	def __str__(self):
		return f"{self.codigo_legivel} - {self.nome}"


class TipoTecnologia(models.Model):
	nome = models.CharField(max_length=100, unique=True)
	descricao = models.TextField(blank=True)

	class Meta:
		ordering = ("nome",)

	def __str__(self):
		return self.nome


class Tecnologia(models.Model):
	nome = models.CharField(max_length=120)
	tipo = models.ForeignKey(TipoTecnologia, related_name="tecnologias", on_delete=models.PROTECT)
	descricao = models.TextField(blank=True)
	vantagens = models.TextField(blank=True)
	desvantagens = models.TextField(blank=True)
	url = models.URLField(blank=True)

	class Meta:
		ordering = ("tipo", "nome")

	def __str__(self):
		return self.nome


class Competencia(models.Model):
	nome = models.CharField(max_length=120)
	descricao = models.TextField(blank=True)

	class Meta:
		ordering = ("nome",)

	def __str__(self):
		return self.nome


class Formacao(models.Model):
	nome = models.CharField(max_length=160)
	instituicao = models.CharField(max_length=160)
	descricao = models.TextField(blank=True)
	ano_inicio = models.PositiveSmallIntegerField(null=True, blank=True)
	ano_fim = models.PositiveSmallIntegerField(null=True, blank=True)
	url = models.URLField(blank=True)

	class Meta:
		ordering = ("-ano_inicio", "nome")

	def __str__(self):
		return self.nome


class Projeto(models.Model):
	titulo = models.CharField(max_length=160)
	resumo = models.CharField(max_length=255, blank=True)
	descricao = models.TextField(blank=True)
	imagem = models.ImageField(upload_to="portfolio/projetos/", blank=True, null=True)
	github_url = models.URLField(blank=True)
	demo_url = models.URLField(blank=True)
	tecnologias = models.ManyToManyField(Tecnologia, related_name="projetos", blank=True)
	competencias = models.ManyToManyField(Competencia, related_name="projetos", blank=True)
	formacoes = models.ManyToManyField(Formacao, related_name="projetos", blank=True)
	data_criacao = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ("-data_criacao", "titulo")

	def __str__(self):
		return self.titulo


class MakingOfEntrada(models.Model):
	data = models.DateField()
	commit_hash = models.CharField(max_length=40)
	iteracao = models.PositiveIntegerField()
	titulo = models.CharField(max_length=160)
	descricao = models.TextField()
	alteracoes = models.TextField(blank=True)
	dificuldades = models.TextField(blank=True)
	resultado = models.TextField(blank=True)

	class Meta:
		ordering = ("-data", "-iteracao")

	def __str__(self):
		return f"{self.data} - {self.titulo}"
