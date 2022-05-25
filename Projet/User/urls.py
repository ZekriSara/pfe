from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import index, quizz, upload, upload2, maj, resultat, adminIndex, login, register, \
    userindex, \
    ajouternorme, upload3, quizz2

urlpatterns = [
    path('home/', index),
    path("login/",login),
    path("register/",register),
    path('quizz/<id>/<test>/', quizz2),
    path('quizz/<id>/', quizz),
    path('ajax/', maj),
    path('resultat/',resultat),
    path('upload/', upload),
    path('upload2/',upload2),
    path('upload3/',upload3),
    path('admin/',adminIndex),
    path('users/',userindex),
    path('ajout/norme/',ajouternorme),

    path("logout/", LogoutView.as_view(), name="logout")

]
