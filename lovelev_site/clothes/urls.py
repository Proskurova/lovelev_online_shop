from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from .views import *

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('category/', Category.as_view(), name='cat'),
    path('popular/', Popular.as_view(), name='popular'),
    path('question_user_form/', question_user_form, name='question_user_form'),
    path('category/<slug:slug>/', ProductCategory.as_view(), name='category'),
    path('information/<slug:slug>/', Information.as_view(), name='information'),
    path('delivery_payment/<slug:slug>/', Information.as_view(), name='delivery_payment'),
    path('<slug:product_slug>/', views.product_detail, name='product_detail'),
]