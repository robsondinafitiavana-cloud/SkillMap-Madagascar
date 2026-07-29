from django.core.management.base import BaseCommand
from skills.models import Skill


SKILLS = [
    ("Python", "LANGAGE"), ("Django", "FRAMEWORK"), ("Java", "LANGAGE"),
    ("JavaScript", "LANGAGE"), ("React", "FRAMEWORK"), ("PHP", "LANGAGE"),
    ("C", "LANGAGE"), ("C++", "LANGAGE"),
    ("Réseaux", "RESEAU"), ("Administration réseau", "RESEAU"),
    ("Linux", "SYSTEME"), ("Windows Server", "SYSTEME"), ("Docker", "SYSTEME"),
    ("Intelligence Artificielle", "IA"), ("Machine Learning", "IA"), ("Deep Learning", "IA"),
    ("Cybersécurité", "CYBER"), ("Sécurité des réseaux", "CYBER"),
    ("Design UI/UX", "DESIGN"), ("Figma", "DESIGN"),
    ("PostgreSQL", "AUTRE"), ("MySQL", "AUTRE"), ("Git", "AUTRE"), ("Gestion de projet", "AUTRE"),
]


class Command(BaseCommand):
    help = "Crée le référentiel de compétences de base pour SkillMap Madagascar"

    def handle(self, *args, **options):
        created = 0
        for name, category in SKILLS:
            _, was_created = Skill.objects.get_or_create(name=name, defaults={"category": category})
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(
            f"{created} nouvelle(s) compétence(s) créée(s). Total : {Skill.objects.count()}."
        ))
