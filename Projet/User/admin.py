from django.contrib import admin
from .models import Norme,Chapitre,SC_niv1,SC_niv2,SC_niv3,Question_Generale,Test,Reponse,Point,FileModel
# Register your models here.

admin.site.register(Norme)
admin.site.register(Chapitre)
admin.site.register(SC_niv1)
admin.site.register(SC_niv2)
admin.site.register(SC_niv3)
admin.site.register(Point)
admin.site.register(Question_Generale)
admin.site.register(Test)
admin.site.register(Reponse)

admin.site.register(FileModel)

