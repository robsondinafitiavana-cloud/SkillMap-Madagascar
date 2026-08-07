"""
Bibliothèque d'icônes SVG pour SkillMap Madagascar.

Pourquoi un système maison plutôt qu'une police d'icônes (Font Awesome,
Material Icons...) ? Parce que ces polices se chargent normalement depuis
un CDN externe — exactement le genre de dépendance qui a déjà causé des
soucis d'affichage sur ce projet (voir le CSS Tailwind, désormais compilé
en local). Ici, chaque icône est un simple <svg> inline, généré par un tag
de template, sans aucun fichier à télécharger ni requête réseau.

Utilisation dans un template :
    {% load icons %}
    {% icon "home" "w-5 h-5" %}

Le premier argument est le nom de l'icône (voir dictionnaire ICONS
ci-dessous), le second est optionnel et correspond aux classes Tailwind
de taille/couleur (par défaut "w-5 h-5").
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Chaque valeur est le contenu interne d'un <svg viewBox="0 0 24 24">,
# dans un style cohérent (traits, sans remplissage) pour que toutes les
# icônes du site se ressemblent visuellement.
ICONS = {
    'home': '<path stroke-linecap="round" stroke-linejoin="round" d="M3 10.5L12 3l9 7.5M5 9.5V20a1 1 0 001 1h4v-5a2 2 0 012-2h0a2 2 0 012 2v5h4a1 1 0 001-1V9.5" />',
    'user': '<circle cx="12" cy="8" r="3.25" /><path stroke-linecap="round" d="M5 20c.8-3.5 3.6-5.5 7-5.5s6.2 2 7 5.5" />',
    'light-bulb': '<path stroke-linecap="round" stroke-linejoin="round" d="M9 18h6M10 21h4M8.5 14.5a4.5 4.5 0 117 0c-.7.75-1.5 1.5-1.5 2.5h-4c0-1-.8-1.75-1.5-2.5zM12 3v1.5M4.5 6.5l1 1M19.5 6.5l-1 1" />',
    'briefcase': '<rect x="3.5" y="8" width="17" height="11" rx="2" /><path stroke-linecap="round" d="M8.5 8V6.5a2 2 0 012-2h3a2 2 0 012 2V8M3.5 12.5h17" />',
    'academic-cap': '<path stroke-linecap="round" stroke-linejoin="round" d="M12 4L2.5 8.5 12 13l9.5-4.5L12 4z" /><path stroke-linecap="round" stroke-linejoin="round" d="M6 10.7V16c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5v-5.3" /><path stroke-linecap="round" d="M21.5 8.5v5" />',
    'clock': '<circle cx="12" cy="13" r="7.5" /><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4l3 2" /><path stroke-linecap="round" d="M9 2.5h6" />',
    'document-text': '<path stroke-linecap="round" stroke-linejoin="round" d="M7 3.5h7l4 4V20a1 1 0 01-1 1H7a1 1 0 01-1-1V4.5a1 1 0 011-1z" /><path stroke-linecap="round" stroke-linejoin="round" d="M14 3.5V8h4" /><path stroke-linecap="round" d="M8.5 12.5h7M8.5 15.5h7M8.5 18.5h4" />',
    'sparkles': '<path stroke-linecap="round" stroke-linejoin="round" d="M11 3l1.2 3.6L16 8l-3.8 1.4L11 13l-1.2-3.6L6 8l3.8-1.4L11 3z" /><path stroke-linecap="round" stroke-linejoin="round" d="M18 13l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7.7-2z" />',
    'magnifying-glass': '<circle cx="10.5" cy="10.5" r="6.5" /><path stroke-linecap="round" d="M20 20l-4.8-4.8" />',
    'inbox': '<path stroke-linecap="round" stroke-linejoin="round" d="M4 12h4l1.5 2.5h5L16 12h4" /><path stroke-linecap="round" stroke-linejoin="round" d="M5 5.5h14a1 1 0 011 1V18a1.5 1.5 0 01-1.5 1.5h-13A1.5 1.5 0 014 18V6.5a1 1 0 011-1z" />',
    'building-office': '<rect x="5" y="4" width="9" height="16" rx="1" /><rect x="14" y="9" width="5" height="11" rx="1" /><path stroke-linecap="round" d="M7.5 7.5h1.5M11 7.5h1.5M7.5 11h1.5M11 11h1.5M7.5 14.5h1.5M11 14.5h1.5M16 12.5h1M16 15.5h1" />',
    'megaphone': '<path stroke-linecap="round" stroke-linejoin="round" d="M3 10v4a1 1 0 001 1h2l6 3.5V5.5L6 9H4a1 1 0 00-1 1z" /><path stroke-linecap="round" d="M17 8.5a4 4 0 010 7M20 6a7.5 7.5 0 010 12" />',
    'plus': '<path stroke-linecap="round" d="M12 5v14M5 12h14" />',
    'chart-bar': '<path stroke-linecap="round" stroke-linejoin="round" d="M4 20V10M10 20V4M16 20v-7M4 20h16" />',
    'cog': '<circle cx="12" cy="12" r="3" /><path stroke-linecap="round" stroke-linejoin="round" d="M12 3.5v2M12 18.5v2M20.5 12h-2M5.5 12h-2M17.7 6.3l-1.4 1.4M7.7 16.3l-1.4 1.4M17.7 17.7l-1.4-1.4M7.7 7.7L6.3 6.3" />',
    'trophy': '<path stroke-linecap="round" stroke-linejoin="round" d="M7 4h10v4a5 5 0 01-10 0V4z" /><path stroke-linecap="round" d="M7 5.5H4.5a1 1 0 00-1 1.2 4 4 0 003.7 3.2M17 5.5h2.5a1 1 0 011 1.2 4 4 0 01-3.7 3.2" /><path stroke-linecap="round" d="M12 12.5V16M9 20h6M9.5 20c0-1.8.7-3 2.5-4 1.8 1 2.5 2.2 2.5 4" />',
    'chat-bubble': '<path stroke-linecap="round" stroke-linejoin="round" d="M4 5.5h16a1 1 0 011 1V15a1 1 0 01-1 1H9l-4.5 3.5V16H4a1 1 0 01-1-1V6.5a1 1 0 011-1z" />',
    'book-open': '<path stroke-linecap="round" stroke-linejoin="round" d="M12 6.5c-1.5-1.2-3.8-2-6.5-2-.6 0-1 .4-1 1V17c0 .6.4 1 1 1 2.7 0 5 .8 6.5 2 1.5-1.2 3.8-2 6.5-2 .6 0 1-.4 1-1V5.5c0-.6-.4-1-1-1-2.7 0-5 .8-6.5 2z" /><path stroke-linecap="round" d="M12 6.5V19" />',
    'bell': '<path stroke-linecap="round" stroke-linejoin="round" d="M6 9.5a6 6 0 1112 0c0 4 1.2 5.5 1.5 6.5H4.5C4.8 15 6 13.5 6 9.5z" /><path stroke-linecap="round" d="M9.5 18.5a2.5 2.5 0 005 0" />',
    'logout': '<path stroke-linecap="round" stroke-linejoin="round" d="M9 4.5H6a1.5 1.5 0 00-1.5 1.5v12a1.5 1.5 0 001.5 1.5h3" /><path stroke-linecap="round" stroke-linejoin="round" d="M14 8l4 4-4 4M18 12H9" />',
    'check-circle': '<circle cx="12" cy="12" r="8.5" /><path stroke-linecap="round" stroke-linejoin="round" d="M8.5 12.3l2.3 2.3 4.7-5.1" />',
    'check': '<path stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7" />',
    'eye': '<path stroke-linecap="round" stroke-linejoin="round" d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z" /><circle cx="12" cy="12" r="2.75" />',
    'pencil': '<path stroke-linecap="round" stroke-linejoin="round" d="M15.5 5.5l3 3L8 19l-4 1 1-4 10.5-10.5z" />',
    'lock-closed': '<rect x="5.5" y="10.5" width="13" height="9" rx="1.5" /><path stroke-linecap="round" d="M8.5 10.5V7.5a3.5 3.5 0 017 0v3" />',
    'banknotes': '<rect x="2.5" y="6.5" width="19" height="11" rx="1.5" /><circle cx="12" cy="12" r="2.5" />',
    'phone': '<path stroke-linecap="round" stroke-linejoin="round" d="M5 4.5h3l1.5 4L7.5 10a11 11 0 006.5 6.5l1.5-2 4 1.5v3a1.5 1.5 0 01-1.6 1.5A16.5 16.5 0 015 6.1 1.5 1.5 0 015 4.5z" />',
    'envelope': '<rect x="3" y="5.5" width="18" height="13" rx="1.5" /><path stroke-linecap="round" stroke-linejoin="round" d="M3.5 6.5L12 13l8.5-6.5" />',
    'map': '<path stroke-linecap="round" stroke-linejoin="round" d="M9 4.5L4 6v13.5l5-1.5m0-13.5l6 1.5m-6-1.5v13.5m6-12l5-1.5v13.5l-5 1.5m0-13.5v13.5m0-13.5L9 18" />',
    'flag': '<path stroke-linecap="round" stroke-linejoin="round" d="M6 3.5v17" /><path stroke-linecap="round" stroke-linejoin="round" d="M6 4.5c2-1 4 .5 6 0s4-1 6 0v8c-2-1-4 .5-6 0s-4-1-6 0z" />',
    'arrow-left': '<path stroke-linecap="round" stroke-linejoin="round" d="M19 12H5M11 6l-6 6 6 6" />',
    'arrow-right': '<path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6" />',
}


@register.simple_tag
def icon(name, css_class="w-5 h-5"):
    """Retourne le SVG inline correspondant à `name`, avec les classes
    Tailwind passées en second argument (taille, couleur...)."""
    inner = ICONS.get(name)
    if inner is None:
        # Icône inconnue : on affiche un petit point plutôt que de casser
        # la page, et ça reste facile à repérer pendant le développement.
        inner = '<circle cx="12" cy="12" r="2" />'
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
        f'stroke-width="1.5" stroke="currentColor" class="{css_class}">{inner}</svg>'
    )
    return mark_safe(svg)
