from rest_framework.permissions import BasePermission
from .models import User


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        try:
            user = User.objects.get(email=request.user.email)
            return user.role == "admin"
        except User.DoesNotExist:
            return False


class IsEmployer(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        try:
            user = User.objects.get(email=request.user.email)
            return user.role == "employer"
        except User.DoesNotExist:
            return False


class IsCandidate(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        try:
            user = User.objects.get(email=request.user.email)
            return user.role == "candidate"
        except User.DoesNotExist:
            return False