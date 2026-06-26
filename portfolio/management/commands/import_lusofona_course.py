import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from portfolio.models import Curso, UnidadeCurricular


def to_text(value):
    if value in (None, ""):
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    if isinstance(value, list):
        parts = [to_text(item) for item in value]
        return "\n".join(part for part in parts if part)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def to_int(value):
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_decimal(value):
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (TypeError, ValueError, ArithmeticError):
        return None


def to_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    value_text = str(value)
    try:
        return date.fromisoformat(value_text[:10])
    except ValueError:
        return None


def to_bool(value):
    return bool(value)


class Command(BaseCommand):
    help = "Importa um curso da Lusófona e as respetivas unidades curriculares a partir de JSONs."

    def add_arguments(self, parser):
        parser.add_argument(
            "course_json",
            help="Ficheiro JSON com o detalhe do curso, por exemplo data/ULHT260-PT.json.",
        )
        parser.add_argument(
            "--json-dir",
            default="data",
            help="Diretório onde estão os JSONs das unidades curriculares.",
        )

    def handle(self, *args, **options):
        course_json_path = Path(options["course_json"])
        json_dir = Path(options["json_dir"])

        if not course_json_path.exists():
            raise CommandError(f"Ficheiro JSON do curso não encontrado: {course_json_path}")

        with course_json_path.open(encoding="utf-8") as file_handle:
            course_payload = json.load(file_handle)

        course_detail = course_payload.get("courseDetail") if isinstance(course_payload, dict) else None
        flat_plan = course_payload.get("courseFlatPlan", []) if isinstance(course_payload, dict) else []
        if not isinstance(course_detail, dict):
            raise CommandError("O JSON do curso não contém a chave 'courseDetail'.")
        if not isinstance(flat_plan, list):
            raise CommandError("O JSON do curso não contém a chave 'courseFlatPlan' como lista.")

        course_code = to_int(course_detail.get("courseCode"))
        if course_code is None:
            raise CommandError("Não foi possível determinar o código do curso.")

        course_defaults = {
            "nome": to_text(course_detail.get("courseName")),
            "grau": to_text(course_detail.get("degree")),
            "plano_curricular_codigo": to_int(course_detail.get("curricularPlanCode")),
            "plano_curricular_nome": to_text(course_detail.get("curricularPlanName")),
            "area_cientifica": to_text(course_detail.get("scientificArea")),
            "codigo_area_cientifica": to_text(course_detail.get("scientificAreaCode")),
            "cnaef": to_text(course_detail.get("scientificAreaCNAEFCode")),
            "ects": to_decimal(course_detail.get("courseECTS")),
            "estado_acreditacao": to_text(course_detail.get("creditationStatus")),
            "codigo_estado_acreditacao": to_text(course_detail.get("creditationStatusCode")),
            "data_publicacao": to_date(course_detail.get("publicationDate")),
            "apresentacao": to_text(course_detail.get("presentation")),
            "objetivos": to_text(course_detail.get("objectives")),
            "saidas_profissionais": to_text(course_detail.get("careerOportunities")),
            "condicoes_acesso": to_text(course_detail.get("accessContidions")),
            "estudos_futuros": to_text(course_detail.get("futureStudies")),
            "contactos_direcao": to_text(course_detail.get("directionContact")),
            "email_direcao": to_text(course_detail.get("directionEmail")),
            "contactos_secretariado": to_text(course_detail.get("courseSecretariatContact")),
            "email_secretariado": to_text(course_detail.get("courseSecretariatEmail")),
            "url": to_text(course_detail.get("courseUrl")),
        }

        with transaction.atomic():
            curso, _ = Curso.objects.update_or_create(
                codigo=course_code,
                defaults=course_defaults,
            )

            imported_units = 0
            for unit in flat_plan:
                if not isinstance(unit, dict):
                    continue

                readable_code = to_text(unit.get("curricularIUnitReadableCode"))
                if not readable_code:
                    continue

                unit_detail_path = json_dir / f"{readable_code}-PT.json"
                unit_detail = {}
                if unit_detail_path.exists():
                    with unit_detail_path.open(encoding="utf-8") as file_handle:
                        unit_detail_payload = json.load(file_handle)
                    if isinstance(unit_detail_payload, dict):
                        unit_detail = unit_detail_payload

                unit_defaults = {
                    "curso": curso,
                    "codigo": to_int(unit.get("curricularUnitCode")) or 0,
                    "nome": to_text(unit.get("curricularUnitName")),
                    "ano": to_int(unit.get("curricularYear")) or 0,
                    "semestre": to_text(unit.get("semester")),
                    "semestre_codigo": to_text(unit.get("semesterCode")),
                    "ects": to_decimal(unit.get("ects")) or Decimal("0"),
                    "grupo_codigo": to_int(unit.get("curricularUnitGroupCode")),
                    "grupo_nome": to_text(unit.get("curricularBranchName")),
                    "ramo_codigo": to_int(unit.get("curricularBranchCode")),
                    "ramo_nome": to_text(unit.get("curricularBranchName")),
                    "opcao_codigo": to_text(unit.get("optionCode")),
                    "opcao": to_text(unit.get("option")),
                    "horas_contacto": to_int(unit.get("hrTotalContacto")),
                    "horas_contacto_int": to_int(unit.get("hrTotalContactoInt")),
                    "mobilidade_entrada": to_bool(unit.get("pubMobIncoming")),
                    "mobilidade_saida": to_bool(unit.get("pubMobOutgoing")),
                    "lingua": to_text(unit_detail.get("language")),
                    "lingua_codigo": to_text(unit_detail.get("languageCode")),
                    "tipo": to_text(unit_detail.get("type")),
                    "natureza": to_text(unit_detail.get("nature")),
                    "diploma": to_text(unit_detail.get("diplomaDegree")),
                    "apresentacao": to_text(unit_detail.get("presentation")),
                    "objetivos": to_text(unit_detail.get("objectives")),
                    "programa": to_text(unit_detail.get("programme")),
                    "metodologia": to_text(unit_detail.get("methodology")),
                    "avaliacao": to_text(unit_detail.get("avaliacao")),
                    "bibliografia": to_text(unit_detail.get("bibliography")),
                    "competencias": to_text(unit_detail.get("competences")),
                }

                UnidadeCurricular.objects.update_or_create(
                    codigo_legivel=readable_code,
                    defaults=unit_defaults,
                )
                imported_units += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Importado o curso {curso.nome} ({curso.codigo}) e {imported_units} unidades curriculares."
            )
        )
