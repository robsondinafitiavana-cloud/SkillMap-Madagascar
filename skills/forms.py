from django import forms
from .models import Skill, StudentSkill


class StudentSkillForm(forms.ModelForm):
    """Formulaire utilisé par l'étudiant pour ajouter/mettre à jour une compétence
    dans son propre profil (choisie dans le référentiel global)."""
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), label="Compétence")

    class Meta:
        model = StudentSkill
        fields = ['skill', 'level']


class SkillCreateForm(forms.ModelForm):
    """Formulaire d'ajout d'une NOUVELLE compétence au référentiel global.

    Accessible aussi bien aux étudiants qu'aux entreprises : si une compétence
    n'existe pas encore dans la liste (ex. un nouveau framework), n'importe quel
    utilisateur connecté peut l'ajouter, elle devient alors disponible pour tout
    le monde (étudiants comme entreprises publiant une offre).
    """
    class Meta:
        model = Skill
        fields = ['name', 'category']
        labels = {'name': 'Nom de la compétence', 'category': 'Catégorie'}

    def clean_name(self):
        # Evite les doublons du type "python" / "Python" / " Python "
        name = self.cleaned_data['name'].strip()
        if Skill.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Cette compétence existe déjà dans le référentiel.")
        return name
