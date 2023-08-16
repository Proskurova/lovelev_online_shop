from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from clothes.models import Product
from .favourites import Favourites


def favourites_add(request, product_id):
    favourites = Favourites(request)

    product = get_object_or_404(Product, id=product_id)
    favourites.add(product=product)
    return redirect('favourites:favourites_detail')


def favourites_remove(request, product_id):
    print(f'Функция favourites_remove: {product_id}')
    favourites = Favourites(request)
    print(f'Функция favourites_remove2: {favourites}')
    product = get_object_or_404(Product, id=product_id)
    favourites.remove(str(product.id))
    return redirect('favourites:favourites_detail')


def favourites_detail(request):
    favourites = Favourites(request)
    return render(request, 'favourites/favourites_detail.html', {'favourites': favourites})