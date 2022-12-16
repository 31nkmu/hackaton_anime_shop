from typing import List

from applications.comments.models import Comment
from applications.comments.serializers import CommentSerializer


def give_comment(obj, user, comment) -> str:
    """
    пользователь ставит комментарий
    :param obj: продукт который комментируют
    :param user: пользователь который комментирует
    :param comment: комментарий
    """
    comment_obj, is_created = Comment.objects.get_or_create(user=user, product=obj)
    comment_obj.comment = comment
    comment_obj.save()
    if is_created:
        return 'Комментарий создан'
    return 'Комментарий обновлен'


def del_comment(obj, user):
    """
    Удаляет комментарий
    :param obj: продукт, комментарий которого удаляют
    :param user: пользователь, комментарий которого удаляют
    """
    try:
        Comment.objects.get(product=obj, user=user).delete()
    except Comment.DoesNotExist:
        pass


def is_commented(obj, user) -> bool:
    """
    Оставлял ли пользователь комментарий
    :param obj: продукт
    :param user: пользователь
    """
    try:
        return Comment.objects.filter(user=user, product=obj).exists()
    except TypeError:
        return False


def get_commentators(obj) -> List[dict]:
    """
    Выводит список комментаторов и комментариев к продукту
    :param obj: продукт, комментарии которого выводятся
    """
    commentators = Comment.objects.filter(product=obj)
    serializer = CommentSerializer(commentators, many=True)
    commentators = [{'user': i['user'], 'comment': i['comment']} for i in serializer.data]
    return commentators


def get_comments(user) -> List[dict]:
    """
    Выводит список комментариев пользователя
    :param user: пользователь, комментарии которого выводятся
    """
    comments = Comment.objects.filter(user=user)
    serializer = CommentSerializer(comments, many=True)
    comments = [{'product': i['product'], 'comment': i['comment']} for i in serializer.data]
    return comments
