from typing import List

from applications.favorites.models import Favorite
from applications.favorites.serializers import FavoriteSerializer


def add_del_favorite(obj, user) -> str:
    """
    Добавляет/удаляет продукт из избранных
    :param obj: продукт который добавляется
    :param user: пользователь который добавляет/удаляет
    """
    fav_obj, is_created = Favorite.objects.get_or_create(product=obj, user=user)
    fav_obj.is_favorite = not fav_obj.is_favorite
    fav_obj.save()
    if fav_obj.is_favorite:
        return 'Добавлено в избранное'
    return 'Удалено из избранных'


def is_favorite(obj, user) -> bool:
    """
    Проверяет, находится ли продукт в избранных у пользователя
    :param obj: продукт
    :param user: пользователь
    """
    try:
        return Favorite.objects.filter(product=obj, user=user, is_favorite=True).exists()
    except TypeError:
        return False


def get_favorites(user) -> List[dict]:
    """
    Выводит избранных список продуктов
    :param user: пользователь который добавил в избранное
    """
    try:
        products = Favorite.objects.filter(user=user, is_favorite=True)
        serializer = FavoriteSerializer(products, many=True)
        return serializer.data
    except TypeError:
        return []
