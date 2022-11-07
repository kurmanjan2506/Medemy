from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(views.UserListView.as_view())), # Для получения всех аккаунтов
    path('<int:pk>/', views.UserDetailView.as_view()), # Для получения детального списка аккаунта
    path('register/', views.RegistrationView.as_view()), # Для регистрации
    path('login/', views.LoginView.as_view()), # Для авторизации
    path('logout/', views.LogoutView.as_view()), # Для выхода
    path('refresh/', TokenRefreshView.as_view()), # ?
    path('forgot/', views.ForgotPasswordView.as_view()), # Для восстановления пароля
    path('restore/', views.RestorePasswordView.as_view()), # Для изменения пароля
    path('follow-spam/', views.FollowSpamApi.as_view()),
]