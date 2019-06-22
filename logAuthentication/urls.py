from django.conf.urls import  url
from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login_auth", views.login_auth, name="login_auth"),
    path("logout", views.log_out, name="logout"),
    path("login/", views.user_login, name="login"),
    path("create_user/", views.create_user, name="create_user"),

]
