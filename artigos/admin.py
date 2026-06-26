from django.contrib import admin

from .models import Artigo, Comentario, Like


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ("pk", "autor", "data_criacao")
    search_fields = ("texto", "autor__username")
    list_filter = ("data_criacao",)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("artigo", "utilizador", "data_criacao")
    search_fields = ("texto", "utilizador__username")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("artigo", "utilizador", "session_key", "data_criacao")
