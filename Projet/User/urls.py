from django.urls import path
from . import views
from .views import index, quizz, csv, upload , upload_files

urlpatterns = [
    path('', index),
    path('quizz/', quizz),
    path('csv/', csv),
    path('upload/', upload),

    path('test/', upload_files),
	
]
