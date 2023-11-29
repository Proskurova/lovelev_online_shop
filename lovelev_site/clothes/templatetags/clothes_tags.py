from django import template
from clothes.forms import QuestionUserForm

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
    question_user_form = QuestionUserForm()
    popup = 'popup_question'
    return {
        "footer_items": footer_items,
        "question_user_form": question_user_form,
        "popup": popup
    }