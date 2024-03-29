from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.decorators import action


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="Авторизация",
        operation_description="Эндпоинт дял получения access и refresh токен"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="JWT Refresh",
        operation_description="Эндпоинт для обновления JWT токена"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class CustomTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_summary="JWT Verify",
        operation_description="Эндпоинт для проверки JWT токена"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class CustomUserViewSet(DjoserViewSet):
    @swagger_auto_schema(
        operation_summary="Регистрация пользователей",
        operation_description="Эндпоинт для создания нового пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        required=['email', 'password', 'name']
        )
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_summary="Мой аккаунт",
        operation_description="Эндпоинт для редактирования учетной записи"
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Активировать аккаунт",
        operation_description="Эндпоинт для активации юзера",
    )
    def activation(self, request, *args, **kwargs):
        return super().activation(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Повторно отправить активацию",
        operation_description="Эндпоинт для повторной активации",
    )
    def resend_activation(self, request, *args, **kwargs):
        return super().resend_activation(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Сменить пароль",
        operation_description="Эндпоинт для смены пароля",
    )
    def set_password(self, request, *args, **kwargs):
        return super().set_password(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Восстановить пароль",
        operation_description="Эндпоинт для восстановления пароля"
    )
    def reset_password(self, request, *args, **kwargs):
        return super().reset_password(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Восстановить пароль (Подтверждение)",
        operation_description="Эндпоинт для подтверждения восстановить пароль"
    )
    def reset_password_confirm(self, request, *args, **kwargs):
        return super().reset_password_confirm(request, *args, **kwargs)
