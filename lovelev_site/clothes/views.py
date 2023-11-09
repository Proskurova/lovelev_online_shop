from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.core.paginator import Paginator
from cart.cart import Cart
from .models import *
from cart.forms import *


class HomeTemplateView(ListView):
    model = Category
    template_name = 'clothes/home.html'
    context_object_name = 'categories'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Меньше одежды — больше комплектов'
        page = Product.objects.all()
        poginator = Paginator(page, 3)
        context['products'] = poginator.get_page(page)
        return context


class ShopView(ListView):
    model = Product
    template_name = 'clothes/product_index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Магазин'
        return context


class Popular(ListView):
    model = Product
    template_name = 'clothes/product_index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Популярное'
        context['products'] = Product.objects.filter(popular=True)
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
    # allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['slug'])

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


# class Delivery(TemplateView):
#     model = MenuItem
#     template_name = 'clothes/delivery.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = MenuItem.objects.get(url=self.kwargs['slug'])
#         return context


