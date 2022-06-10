from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

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
    path('resultat/<id>',resultat),
    path('upload/', upload),
    path('upload2/',upload2),
    path('upload3/',upload3),
    path('admin/',adminIndex),
    path('users/',userindex),
    path('normes/',normes),
    path('lois/', lois),
    path('ajout/norme/',ajouternorme),
    path('ajout/loi/',indexloi),
    path('historique/',hist),
    path('uploadloi/',ajouterloi),
    path('norme/',normeuser),
    path('loi/',loiuser),
    path('ajout/admin/',ajouteradmin),
    path("ajoutad/",ajoutad),
    path("admins/",listeadmins),
    path("delete/<id>/",deleteuser),
    path("valider/<id>",valideruser),
    path("supp/<id>/",deleteloi),
    path("sup/<id>/",deletenorme),
    path("voir/<id>/",voir),
    path("norme/<id>/",voirnorme),
    path("loi/<id>/",voirloi),


    path('khra/',khra),

    path("logout/", logo, name="logout")

]

