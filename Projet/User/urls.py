from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import index, quizz, upload, upload2, maj, resultat, adminIndex, log, register, \
    userindex, \
    ajouternorme, upload3, quizz2, reg, cnx, hist, khra, prec

urlpatterns = [
    path('home/', index),
    path("login/",log),
    path("register/",register),
    path("inscription/",reg),
    path("cnx/",cnx),
    path('quizz/<id>/<test>/', quizz2),
    path('quizz/<id>/', quizz),
    path('ajax/', maj),
    path('prec/', prec),
    path('resultat/',resultat),
    path('upload/', upload),
    path('upload2/',upload2),
    path('upload3/',upload3),
    path('admin/',adminIndex),
    path('users/',userindex),
    path('ajout/norme/',ajouternorme),
    path('historique/',hist),

    path('khra',khra),

    path("logout/", LogoutView.as_view(), name="logout")

]

