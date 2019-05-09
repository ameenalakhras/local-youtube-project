from django.conf.urls import  url
from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainPage, name="mainPage"),
    path("temp/", views.temp, name="tempPage")

]
