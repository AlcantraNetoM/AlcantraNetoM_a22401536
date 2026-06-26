import json
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Importa registos a partir de um ficheiro JSON para um modelo Django."

    def add_arguments(self, parser):
        parser.add_argument(
            "model_label",
            help="Etiqueta do modelo no formato app_label.ModelName, por exemplo portfolio.TFC",
        )
        parser.add_argument(
            "--json-path",
            default="data/tfcs.json",
            help="Caminho para o ficheiro JSON a importar.",
        )

    def handle(self, *args, **options):
        model_label = options["model_label"]
        json_path = Path(options["json_path"])

        try:
            app_label, model_name = model_label.split(".", 1)
        except ValueError as exc:
            raise CommandError(
                "O parâmetro model_label deve usar o formato app_label.ModelName."
            ) from exc

        model = apps.get_model(app_label, model_name)
        if model is None:
            raise CommandError(f"Modelo não encontrado: {model_label}")

        if not json_path.exists():
            raise CommandError(f"Ficheiro JSON não encontrado: {json_path}")

        with json_path.open(encoding="utf-8") as file_handle:
            payload = json.load(file_handle)

        if isinstance(payload, dict):
            if "items" in payload:
                records = payload["items"]
            elif "data" in payload:
                records = payload["data"]
            else:
                raise CommandError(
                    "O JSON deve ser uma lista de objetos ou conter a chave 'items'/'data'."
                )
        elif isinstance(payload, list):
            records = payload
        else:
            raise CommandError("O JSON deve conter uma lista de objetos ou um dicionário válido.")

        if not records:
            self.stdout.write(self.style.WARNING("Nenhum registo encontrado no JSON."))
            return

        created_count = 0
        with transaction.atomic():
            for record in records:
                if not isinstance(record, dict):
                    raise CommandError("Cada registo do JSON deve ser um objeto/dicionário.")
                model.objects.create(**record)
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Importados {created_count} registos para {model._meta.label} a partir de {json_path}."
            )
        )
