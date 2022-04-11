from django.urls import path

from .views import index, quizz

urlpatterns = [
    path('', index),
    path('quizz/', quizz),
]
