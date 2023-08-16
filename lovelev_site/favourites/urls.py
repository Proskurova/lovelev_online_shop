from django.urls import path
from . import views

app_name = 'favourites'


urlpatterns = [
    path('', views.favourites_detail, name='favourites_detail'),
    path('add/<int:product_id>/',
         views.favourites_add,
         name='favourites_add'),
    path('remove/<int:product_id>/',
         views.favourites_remove,
         name='favourites_remove'),
]