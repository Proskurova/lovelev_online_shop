from .favourites import Favourites


def favourites(request):
    return {'favourites': Favourites(request)}