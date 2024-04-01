from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, CustomUserViewSet


urlpatterns = [
    path('users/activations/', CustomUserViewSet.as_view({"post": "activation"}), name="user-activation"),
    path('users/resend_activation/', CustomUserViewSet.as_view({"post": "resend_activation"}), name="user-resend-activation"),
    path('users/', CustomUserViewSet.as_view({"post": "create"}), name="user-list"),
    path('users/set_password/', CustomUserViewSet.as_view({"post": "set_password"}), name="user-set-password"),
    path('users/reset_password/', CustomUserViewSet.as_view({"post": "reset_password"}), name="user-reset-password"),
    path('users/rest_password_confirm/', CustomUserViewSet.as_view({"post": "reset_password_confirm"})),
    path('users/me/', CustomUserViewSet.as_view({
        "get": "me",
        "put": "me",
        "patch": "me",
        "delete": "me"}), name="users-me"),

    path('login/jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('logit/jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('login/jwt/verify/', CustomTokenVerifyView.as_view(), name='jwt-verify')

]
