from django import template
import locale

register = template.Library()

@register.filter
def currency(value):
    # Convierte el valor a un número en coma flotante
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    # Establece la configuración regional para obtener el formato de moneda adecuado
    locale.setlocale(locale.LC_ALL, '')

    # Formatea el valor como moneda y devuelve el resultado
    return locale.currency(value, grouping=True)
