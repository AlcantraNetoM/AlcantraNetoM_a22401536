from django.conf import settings
from django.db import models


class Artigo(models.Model):
    texto = models.TextField()
    fotografia = models.ImageField(upload_to="artigos/", blank=True, null=True)
    link_externo = models.URLField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="artigos")
    class Meta:
        ordering = ("-data_criacao",)

    def __str__(self):
        return f"Artigo #{self.pk}"


class Like(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name="likes")
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=64, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-data_criacao",)

    def __str__(self):
        return f"Like em {self.artigo_id}"


class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name="comentarios")
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("data_criacao",)

    def __str__(self):
        return f"Comentário de {self.utilizador}"
