from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class IsAuthenticatedOrAnon(permissions.IsAuthenticated):
    """
    Same permissions as IsAuthenticated but will allow unauthenticated
    requests to create a new user.
    """

    def has_permission(self, request, view):
        """
        Allows POST requests from unauthenticated users and admin only.
        """
        if request.method in permissions.SAFE_METHODS:
            return super(IsAuthenticatedOrAnon, self).has_permission(request, view)
        if request.method == "POST" and (isinstance(request.user, AnonymousUser) or request.user.is_staff):
            return True
        else:
            return False
