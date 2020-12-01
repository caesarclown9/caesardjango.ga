from rest_framework.permissions import (
    BasePermission, SAFE_METHODS
)



class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.author == request.user
        else:
            return False
