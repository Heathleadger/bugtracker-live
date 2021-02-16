from django.urls import path
from .views import registration, loginPage, logout_view, account_assignment
from rest_framework.authtoken import views

app_name = 'accounts'
urlpatterns = [
    path('registration', registration, name='registration'),
    path('login', loginPage, name="login"),
    path('logout', logout_view, name="logout"),
    path('account-assignment/', account_assignment, name="account-assignment"),
    # path('api-token-auth/', views.obtain_auth_token)
]
