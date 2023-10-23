# Здесь будут указаны все endpoints сайта

from django.urls import path

from shoppers.views import (
    LoginView,
    LogoutView,
    RegisterShopperView,
    UpdateShopperView,
        )

urlpatterns = [
        path('sign-in', LoginView.as_view(), name='sign_in'),
        path('sign-out', LogoutView.as_view(), name='sign_out'),
        path('sign-up', RegisterShopperView.as_view(), name='sign_up'),
        path('profile', UpdateShopperView.as_view(), name='profile'),
        ]
