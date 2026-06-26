from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ArtigoForm, ComentarioForm
from .models import Artigo, Comentario, Like


def artigo_list_view(request):
    artigos = Artigo.objects.select_related("autor").prefetch_related("comentarios__utilizador", "likes").all()
    return render(request, "artigos/artigo_list.html", {"artigos": artigos})


def artigo_detail_view(request, pk):
    artigo = get_object_or_404(Artigo.objects.select_related("autor").prefetch_related("comentarios__utilizador", "likes"), pk=pk)
    comentario_form = ComentarioForm() if request.user.is_authenticated else None
    return render(request, "artigos/artigo_detail.html", {"artigo": artigo, "comentario_form": comentario_form})


class AutorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name="autores").exists()


class ArtigoAutorMixin(AutorRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = getattr(self, "object", None)
        if obj is None:
            return self.request.user.is_authenticated and self.request.user.groups.filter(name="autores").exists()
        return self.request.user.is_authenticated and self.request.user.groups.filter(name="autores").exists() and obj.autor == self.request.user


class ArtigoCreateView(AutorRequiredMixin, CreateView):
    model = Artigo
    form_class = ArtigoForm
    template_name = "artigos/artigo_form.html"
    success_url = reverse_lazy("artigos-list")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class ArtigoUpdateView(ArtigoAutorMixin, UpdateView):
    model = Artigo
    form_class = ArtigoForm
    template_name = "artigos/artigo_form.html"
    success_url = reverse_lazy("artigos-list")


class ArtigoDeleteView(ArtigoAutorMixin, DeleteView):
    model = Artigo
    template_name = "artigos/artigo_confirm_delete.html"
    success_url = reverse_lazy("artigos-list")


@login_required
def comentar_artigo_view(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    form = ComentarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comentario = form.save(commit=False)
        comentario.artigo = artigo
        comentario.utilizador = request.user
        comentario.save()
        return redirect("artigos-detail", pk=pk)
    return render(request, "artigos/artigo_detail.html", {"artigo": artigo, "comentario_form": form})


@login_required
def like_artigo_view(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.user.is_authenticated:
        like = Like.objects.filter(artigo=artigo, utilizador=request.user).first()
    else:
        if not request.session.session_key:
            request.session.save()
        like = Like.objects.filter(artigo=artigo, session_key=request.session.session_key).first()
    if like:
        like.delete()
    else:
        Like.objects.create(
            artigo=artigo,
            utilizador=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if not request.user.is_authenticated else "",
        )
    return redirect("artigos-detail", pk=pk)
