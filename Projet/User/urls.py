from django.urls import path

from .views import index, quizz, maj, resultat

urlpatterns = [
    path('', index),
    path('quizz/<id>/', quizz),
    path('ajax/', maj),
    path('result/',resultat),
]
