from django.apps import apps
from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_portfolio_groups(sender, **kwargs):
    if sender.name not in {"portfolio", "artigos", "accounts"}:
        return

    gestor_group, _ = Group.objects.get_or_create(name="gestor-portfolio")
    autor_group, _ = Group.objects.get_or_create(name="autores")

    portfolio_models = [
        "Curso",
        "UnidadeCurricular",
        "TipoTecnologia",
        "Tecnologia",
        "Competencia",
        "Formacao",
        "Projeto",
        "MakingOfEntrada",
    ]
    portfolio_permissions = []
    for model_name in portfolio_models:
        model = apps.get_model("portfolio", model_name)
        for action in ("add", "change", "delete", "view"):
            perm = Permission.objects.filter(
                content_type__app_label="portfolio",
                codename=f"{action}_{model._meta.model_name}",
            ).first()
            if perm:
                portfolio_permissions.append(perm)

    gestor_group.permissions.set(portfolio_permissions)

    gestor_user, created = User.objects.get_or_create(
        username="gestor-portfolio",
        defaults={"is_staff": True, "is_superuser": False},
    )
    if created:
        gestor_user.set_password("gestor-portfolio")
    gestor_user.is_staff = True
    gestor_user.save()
    gestor_user.groups.add(gestor_group)

    artigo_model = apps.get_model("artigos", "Artigo")
    artigo_perms = []
    for action in ("add", "change", "delete", "view"):
        perm = Permission.objects.filter(
            content_type__app_label="artigos",
            codename=f"{action}_{artigo_model._meta.model_name}",
        ).first()
        if perm:
            artigo_perms.append(perm)
    autor_group.permissions.set(artigo_perms)
