from django.apps import apps
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_author_group(sender, **kwargs):
    if sender.name != "artigos":
        return
    Group.objects.get_or_create(name="autores")
