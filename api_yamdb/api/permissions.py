from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Разрешает доступ администратору или суперпользователю"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
            or request.user.is_superuser
            or request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):
    """Разрешает доступ администратору или суперпользователю,
    остальным только для чтения"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.is_admin
            )
        )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_admin


class IsModeratorOrReadOnly(BasePermission):
    """Разрешает доступ модератору, остальным только для чтения"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_moderator


class IsAuthorOrReadOnly(BasePermission):
    """Разрешает доступ автору, остальным только для чтения"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
