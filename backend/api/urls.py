# Здесь будут указаны все endpoints сайта

from django.urls import path

from profile_users.views import (
    SignInAPIView,
    SignOutAPIView,
    SignUpAPIView,
    ProfileAPIView,
    AvatarChangeAPIView,
    PasswordChangeAPIView,

        )

urlpatterns = [
        path('sign-in', SignInAPIView.as_view(), name='sign_in'),
        path('sign-out', SignOutAPIView.as_view(), name='sign_out'),
        path('sign-up', SignUpAPIView.as_view(), name='sign_up'),
        path('profile', ProfileAPIView.as_view(), name='profile'),
        path('profile/avatar', AvatarChangeAPIView.as_view(), name='avatar_change'),
        path('profile/password', PasswordChangeAPIView.as_view(), name='password_change'),
        ]
