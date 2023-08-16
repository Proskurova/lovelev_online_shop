from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from .models import *
from cart.forms import *


class HomeTemplateView(ListView):
    model = Product
    template_name = 'clothes/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lovelev одежда сделанная с любовью'
        return context


class ProductCategory(ListView):
    model = Product
    template_name = 'clothes/home.html'
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
    return render(request, 'clothes/product_detail.html', {'product': product, 'cart_product_form': cart_product_form})


class Information(TemplateView):
    model = MenuItem
    template_name = 'clothes/information.html'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = MenuItem.objects.get(url=self.kwargs['slug'])
        return context


class Delivery(TemplateView):
    template_name = 'clothes/delivery.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка и оплата'
        return context


