from django.db import models


class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        ordering = ("nome",)

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=120)
    imagem = models.ImageField(upload_to="cursos/")
    professor = models.ForeignKey(
        Professor,
        related_name="cursos",
        on_delete=models.CASCADE,
    )
    alunos = models.ManyToManyField("Aluno", related_name="cursos")

    class Meta:
        ordering = ("nome",)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ("nome",)

    def __str__(self):
        return f"{self.numero} - {self.nome}"
