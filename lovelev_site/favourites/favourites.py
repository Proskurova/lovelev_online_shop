import copy

from django.conf import settings
from clothes.models import Product


class Favourites(object):

    def __init__(self, request):
        """
        Инициализация избранного
        """
        self.session = request.session
        favourites = self.session.get(settings.FAVOURITES_SESSION_ID)
        if not favourites:
            # сохраняем ПУСТУЮ избранное в сессии
            favourites = self.session[settings.FAVOURITES_SESSION_ID] = {}
        self.favourites = favourites

    def __len__(self):
        Fsum = 0
        for item in self.favourites.values():
            Fsum += 1
        return Fsum

    def __iter__(self):
        """
        Перебираем товары в избранном и получаем товары из базы данных.
        """
        # self.favourites.clear()
        product_ids = self.favourites.keys()
        # получаем товары и добавляем их в избранное
        products = Product.objects.filter(id__in=product_ids)

        favourites = copy.deepcopy(self.favourites)
        for product in products:
            favourites[str(product.id)]['product'] = product

        for item in favourites.values():
            yield item

    def add(self, product):
        """
        Добавляем товар в избранное или обновляем его количество.
        """
        product_id = str(product.id)
        if product_id not in self.favourites:
            self.favourites[product_id] = {'price': str(product.price)}
        self.save()

    def save(self):
        # сохраняем товар
        self.session.modified = True

    def remove(self, product_id):
        """
        Удаляем товар
        """
        if product_id in self.favourites:
            del self.favourites[product_id]
            self.save()

    def clear(self):
        # очищаем избранное в сессии
        del self.session[settings.FAVOURITES_SESSION_ID]
        self.save()