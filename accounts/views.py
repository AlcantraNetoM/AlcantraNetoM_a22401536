from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, MagicLinkRequestForm, RegisterForm


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            autores_group, _ = Group.objects.get_or_create(name="autores")
            user.groups.add(autores_group)
            login(request, user)
            return redirect("portfolio-home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("portfolio-home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("portfolio-home")
    magic_form = MagicLinkRequestForm(request.POST or None)
    if request.method == "POST" and "magic-link" in request.POST and magic_form.is_valid():
        email = magic_form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = request.build_absolute_uri(f"/accounts/magic/{uid}/{token}/")
            send_mail(
                "O seu magic link",
                f"Abra este link para entrar: {link}",
                getattr(settings, "DEFAULT_FROM_EMAIL", "webmaster@localhost"),
                [email],
            )
            messages.success(request, "Foi enviado um magic link para o seu email.")
            return render(request, "accounts/magic_sent.html")
        else:
            messages.error(request, "Não existe utilizador com esse email.")
    return render(request, "accounts/login.html", {"form": form, "magic_form": magic_form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts-login")


@require_http_methods(["GET"])
def magic_link_login_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user and default_token_generator.check_token(user, token):
        login(request, user)
        return redirect("portfolio-home")
    messages.error(request, "Magic link inválido ou expirado.")
    return redirect("accounts-login")
