from django.urls import path

from .views import index, quizz, csv, upload, upload_files, maj, resultat

urlpatterns = [
    path('', index),
    path('quizz/<id>/', quizz),
    path('ajax/', maj),
    path('result/',resultat),
    path('csv/', csv),
    path('upload/', upload),
    path('test/', upload_files),

]
