from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        # If it is a GET -> list or retrieve request, then allow access
        if request.method in permissions.SAFE_METHODS:
            return True
        # if the user is an admin, then allow access
        else:
            return bool(request.user and request.user.is_staff)


class IsReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Check permission for read-only requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check permission for write requests
        else:
            return obj.review_user == request.user or request.user.is_staff
