from django.core.management.base import BaseCommand

from skills.models import Skill
from skillmap_ai.knowledge_base import CAREERS, SKILL_CATEGORY_HINTS
from skillmap_ai.models import Career, CareerSkill


class Command(BaseCommand):
    help = "Charge la base de connaissances des métiers (Conseiller de carrière IA)."

    def handle(self, *args, **options):
        nb_careers, nb_links, nb_new_skills = 0, 0, 0

        for entry in CAREERS:
            career, created = Career.objects.update_or_create(
                name=entry['name'],
                defaults={
                    'domain': entry.get('domain', ''),
                    'description': entry.get('description', ''),
                    'recommended_level': entry.get('recommended_level', ''),
                    'desired_experience': entry.get('desired_experience', ''),
                    'average_salary': entry.get('average_salary', ''),
                    'growth_prospects': entry.get('growth_prospects', ''),
                },
            )
            nb_careers += created

            for skill_name in entry.get('required', []):
                skill, was_created = self._get_or_create_skill(skill_name)
                nb_new_skills += was_created
                _, link_created = CareerSkill.objects.update_or_create(
                    career=career, skill=skill, defaults={'importance': 'REQUIRED'},
                )
                nb_links += link_created

            for skill_name in entry.get('recommended', []):
                skill, was_created = self._get_or_create_skill(skill_name)
                nb_new_skills += was_created
                _, link_created = CareerSkill.objects.update_or_create(
                    career=career, skill=skill, defaults={'importance': 'RECOMMENDED'},
                )
                nb_links += link_created

        self.stdout.write(self.style.SUCCESS(
            f"{len(CAREERS)} métier(s) chargé(s) ({nb_careers} nouveau(x)), "
            f"{nb_links} lien(s) compétence-métier créé(s), {nb_new_skills} compétence(s) ajoutée(s) au référentiel."
        ))

    def _get_or_create_skill(self, name):
        category = SKILL_CATEGORY_HINTS.get(name, 'AUTRE')
        return Skill.objects.get_or_create(name=name, defaults={'category': category})
