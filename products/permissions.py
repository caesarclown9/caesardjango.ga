from rest_framework.permissions import (
    BasePermission, SAFE_METHODS
)

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_seller

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return (
                    request.user and request.user.is_authenticated
                    and request.user == obj.author
                    and request.user.is_seller and obj.author.is_seller
            )


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

