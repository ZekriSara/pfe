from django.urls import path
<<<<<<< HEAD

from .views import index, quizz, maj, resultat

urlpatterns = [
    path('', index),
    path('quizz/<id>/', quizz),
    path('ajax/', maj),
    path('result/',resultat),
=======
from . import views
from .views import index, quizz, csv, upload , upload_files

urlpatterns = [
    path('', index),
    path('quizz/', quizz),
    path('csv/', csv),
    path('upload/', upload),

    path('test/', upload_files),
	
>>>>>>> a85016fe155dd3acb43b32c33f324f3b77484163
]
