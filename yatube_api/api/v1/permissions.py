from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    message = 'Только автор может редактировать контент.'

    def has_object_permission(self, request, view, obj):
        # Во всех источниках этот метод определен через if,
        # не нашёл способа записать это одной строкой...
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author
