from django import template
from clothes.forms import QuestionUserForm

from clothes.models import MenuItem
from cart.cart import Cart
register = template.Library()


@register.inclusion_tag('clothes/menu.html', takes_context=True)
def show_menu(context):
    menu_items = MenuItem.objects.filter(level=1)
    # cart = Cart()
    return {
        "menu_items": menu_items,
        # "card": cart,
    }


@register.inclusion_tag('clothes/footer.html', takes_context=True)
def show_footer(context):
    question_user_form = QuestionUserForm()
    popup = 'popup_question'
    return {
        "question_user_form": question_user_form,
        "popup": popup
    }