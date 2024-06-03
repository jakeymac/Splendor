from django.urls import path, include
from Accounts import views as views


urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login_page, name='login'),
    path("logout/", views.logout_view, name='logout'),
]