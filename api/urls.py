from django.urls import path

from users import views as users_views

urlpatterns = [
    path(
        "token/",
        users_views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        users_views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
