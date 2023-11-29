from .forms import QuestionUserForm


def question_user_form(request):
    return {'question_user_form': QuestionUserForm(request)}