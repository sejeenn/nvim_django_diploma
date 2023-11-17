from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Импорт классов, связанных с операциями над аккаунтом пользователя
from myauth.views import (
    SignOutAPIView,
    SignInAPIView,
    SignUpAPIView,
    ProfileUserAPIView,
    AvatarChangeAPIView,
    ChangePasswordAPIView,
)

from shopapp.views import (
    CategoryListView,
    CatalogListAPIView,
    BannerListAPIView,
    PopularListAPIView,
    LimitedListAPIView,
    ProductDetailsAPIView,
    ProductReviewAPIView,
    TagsListAPIView,
)

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),

    # Конечные точки, связанные с операциями над аккаунтом пользователя
    path('sign-out', SignOutAPIView.as_view()),
    path('sign-in', SignInAPIView.as_view()),
    path('sign-up', SignUpAPIView.as_view()),
    path('profile', ProfileUserAPIView.as_view()),
    path('profile/avatar', AvatarChangeAPIView.as_view()),
    path('profile/password', ChangePasswordAPIView.as_view()),

    path('categories', CategoryListView.as_view()),
    path('catalog', CatalogListAPIView.as_view()),
    path('banners', BannerListAPIView.as_view()),
    path('tags', TagsListAPIView.as_view()),
    path('products/popular', PopularListAPIView.as_view()),
    path('products/limited', LimitedListAPIView.as_view()),
    path('product/<int:id>', ProductDetailsAPIView.as_view()),
    path('product/<int:id>/reviews', ProductReviewAPIView.as_view()),
]
