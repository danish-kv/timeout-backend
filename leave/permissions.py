from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
    

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_superuser
    
