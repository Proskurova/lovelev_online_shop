from django import template
from clothes.models import MenuItem
register = template.Library()


@register.inclusion_tag('clothes/menu.html', takes_context=True)
def show_menu(context):
    menu_items = MenuItem.objects.filter(level=1)
    return {
        "menu_items": menu_items,
    }


@register.inclusion_tag('clothes/footer.html', takes_context=True)
def show_footer(context):
    footer_items = MenuItem.objects.filter(level=1)
    return {
        "footer_items": footer_items,
    }