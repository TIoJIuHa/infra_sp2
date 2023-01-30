from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, registration_view, verification_view

router = DefaultRouter()

router.register("v1/users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("v1/auth/signup/", registration_view),
    path("v1/auth/token/", verification_view),
]
