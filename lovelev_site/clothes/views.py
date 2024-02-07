from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView
from django.core.paginator import Paginator
from .models import *
from cart.forms import *
from django.shortcuts import render
from .forms import QuestionUserForm
from .tasks import send_question


from django.http import JsonResponse


class HomeTemplateView(ListView):
    model = Category
    template_name = 'clothes/home.html'
    context_object_name = 'categories'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Меньше одежды — больше комплектов'
        page = Product.objects.filter(popular='True').select_related('cat')
        poginator = Paginator(page, 3)
        products = poginator.get_page(page)
        numbers = range(1, len(products)+1)
        context['products'] = zip(products, numbers)
        return context


class ShopView(ListView):
    model = Product
    template_name = 'clothes/product_index.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.filter(available='True').select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Магазин'
        return context


class Popular(ListView):
    model = Product
    template_name = 'clothes/product_index.html'
    context_object_name = 'products'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(popular='True').select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Популярное'
        return context


class Category(ListView):
    model = Category
    template_name = 'clothes/category.html'
    context_object_name = 'categories'
    paginate_by = 8
    # allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = MenuItem.objects.get(url='category')
        return context


class ProductCategory(ListView):
    model = Product
    template_name = 'clothes/product_index.html'
    context_object_name = 'products'
    paginate_by = 8
    # allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['slug'], available='True').select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = MenuItem.objects.get(url=self.kwargs['slug'])
        return context


def product_detail(request: WSGIRequest, product_slug: str) -> HttpResponse:
    product = get_object_or_404(Product,
                                slug=product_slug,
                                available=True)
    cart_product_form = CartAddProductForm(product.pk)
    sizes = TableSizes.objects.all()
    return render(request, 'clothes/product_detail.html', {'product': product, 'cart_product_form': cart_product_form, 'sizes': sizes}, )


class Information(ListView):
    model = Information
    template_name = 'clothes/information.html'
    context_object_name = 'content'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = MenuItem.objects.get(url=self.kwargs['slug'])
        return context


def question_user_form(request):
    if request.method == 'POST':
        form = QuestionUserForm(request.POST)
        if form.is_valid():
            data = {
                'username': form.cleaned_data['username'],
                'phone': form.cleaned_data['phone'],
                'question': form.cleaned_data['question'],
                'approval': form.cleaned_data['approval'],
            }
            send_question.delay(data)
            # send_question(data)
            return JsonResponse({'success': True})
        else:
            data = {
                'success': False,
                'errors': form.errors.as_json(),
            }
            result = JsonResponse(data)
            return result
    else:
        form = QuestionUserForm(request)
        data = {
            'success': False,
            'errors': form.errors.as_json(),
            'question_user_form': question_user_form
        }
    return JsonResponse(data)




