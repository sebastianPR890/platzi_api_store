from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Páginas de Vistas
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),

    # Endpoints de API
    path('api/register/', views.register_api, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/logout/', views.logout_api, name='api_logout'), # <-- URL para cerrar sesión
    path('api/profile/', views.user_profile_api, name='api_profile'),
    path('api/check-username/', views.check_username_api, name='check_username'),
]