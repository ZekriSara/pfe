from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import index, quizz, csv, upload, upload2, upload_files, maj, resultat, adminIndex, login, register, \
    userindex, \
    ajouternorme, upload3

urlpatterns = [
    path('', index),
    path('quizz/<id>/', quizz),
    path('ajax/', maj),
    path('result/',resultat),
    path('upload/', upload),
    path('upload2/',upload2),
    path('upload3/',upload3),
    path('test/', upload_files),
    path('admin/',adminIndex),
    path('users/',userindex),
    path('ajout/norme/',ajouternorme),

    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")

]
