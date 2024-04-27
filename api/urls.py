from django.urls import path

from users import views as users_views

urlpatterns = [
    path(
        "token/",
        users_views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]
