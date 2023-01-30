from rest_framework import mixins, viewsets


class ListDestroyCreateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Создали собственный вьюсет, для класса подписок,
    для более удобной реализации определенных ограничений по ТЗ
    """

    pass
