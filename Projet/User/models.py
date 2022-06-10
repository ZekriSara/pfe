from tabnanny import verbose
from tkinter import CASCADE

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone


class Client(models.Model):
    id_client= models.AutoField(primary_key=True)
    id_user= models.ForeignKey(User, verbose_name="users",on_delete=models.CASCADE)
    raison=models.TextField()
    num_fisc=models.TextField(default=None, null= True, blank=True)
    is_valid=models.BooleanField(default=False)
    date_fin=models.DateTimeField(default=None, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self) -> str:
        return self.raison

class Admin(models.Model):
    id_admin= models.AutoField(primary_key=True)
    id_user= models.ForeignKey(User, verbose_name="users",on_delete=models.CASCADE)
    is_super=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Admins"

    def __str__(self) -> str:
        return self.id_admin

class Loi(models.Model):
    id = models.TextField(primary_key=True)
    titre = models.TextField()
    descriptif = models.TextField(default=None, blank=True, null=True)
    file_name= models.FileField(upload_to=settings.MEDIA_ROOT+"/pdf",default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Lois"

    def __str__(self) -> str:
        return self.titre

class Norme(models.Model):
    id = models.TextField(primary_key=True)
    titre = models.TextField()
    version = models.IntegerField(default=None, blank=True, null=True)
    descriptif = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Normes"

    def __str__(self) -> str:
        return self.titre


class Chapitre(models.Model):
    id_chap = models.TextField(primary_key=True)
    id_norme = models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    version = models.IntegerField()
    titre = models.TextField()
    descriptif = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Chapitres"

    def __str__(self) -> str:
        return self.titre


class SC_niv1(models.Model):
    id_norme = models.ForeignKey(Norme, verbose_name="Normes", on_delete=models.CASCADE)
    version = models.IntegerField()
    id_chap = models.ForeignKey(Chapitre, verbose_name="Chapitres", on_delete=models.CASCADE)
    id_Sc1 = models.TextField(primary_key=True)
    titre = models.TextField()
    objectif = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sc_niv1"

    def __str__(self) -> str:
        return self.titre


class SC_niv2(models.Model):
    id_norme = models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    version = models.IntegerField()
    id_chap = models.ForeignKey(Chapitre, verbose_name=("Chapitres"), on_delete=models.CASCADE)
    id_Sc1 = models.ForeignKey(SC_niv1, verbose_name=("Sc_niv1"), on_delete=models.CASCADE)
    id_Sc2 = models.TextField(primary_key=True)
    titre = models.TextField()
    objectif = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sc_niv2"

    def __str__(self) -> str:
        return self.titre


class SC_niv3(models.Model):
    id_norme = models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    version = models.IntegerField()
    id_chap = models.ForeignKey(Chapitre, verbose_name="Chapitres", on_delete=models.CASCADE)
    id_Sc1 = models.ForeignKey(SC_niv1, verbose_name=("Sc_niv1"), on_delete=models.CASCADE)
    id_Sc2 = models.ForeignKey(SC_niv2, verbose_name=("Sc_niv2"), on_delete=models.CASCADE)
    id_Sc3 = models.TextField(primary_key=True)
    titre = models.TextField()
    objectif = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sc_niv3"

    def __str__(self) -> str:
        return self.titre


class Point(models.Model):
    id_point = models.TextField(primary_key=True, default="default-id")
    id_norme = models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    version = models.IntegerField()
    id_chap = models.ForeignKey(Chapitre, verbose_name="Chapitres", on_delete=models.CASCADE)
    id_Sc1 = models.ForeignKey(SC_niv1, verbose_name=("Sc_niv1"), on_delete=models.CASCADE, default=None, blank=True,
                               null=True)
    id_Sc2 = models.ForeignKey(SC_niv2, verbose_name=("Sc_niv2"), on_delete=models.CASCADE, default=None, blank=True,
                               null=True)
    id_Sc3 = models.ForeignKey(SC_niv3, verbose_name=("Sc_niv3"), on_delete=models.CASCADE, default=None, blank=True,
                               null=True)
    titre = models.TextField(default=None, blank=True, null=True)
    point = models.TextField()
    type_actif = models.TextField(default=None, blank=True, null=True)
    fct_sec = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Points"

    def __str__(self) -> str:
        return self.titre


class Test(models.Model):
    id_test = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(User,verbose_name=("Users"),on_delete=models.CASCADE,default=None,blank=True, null=True)
    id_norme = models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    finished = models.BooleanField()
    date = models.DateField(default=None, blank=True, null=True)
    last_point = models.TextField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tests"

    def __str__(self) -> str:
        return self.id_test


class Question(models.Model):
    id_qst = models.TextField(primary_key=True)
    id_norme = models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    id_point= models.ForeignKey(Point, verbose_name="Points", on_delete=models.CASCADE, default=None, blank=True, null=True)
    question = models.TextField()
    version = models.IntegerField()


    class Meta:
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return self.id_qst


class Reponse(models.Model):
    id_reponse=models.TextField(primary_key=True)
    id_test=models.ForeignKey(Test,verbose_name="Tests",on_delete=models.CASCADE)
    id_qst=models.ForeignKey(Question,verbose_name="Questions",on_delete=models.SET_NULL,default=None, blank=True, null=True)
    version=models.IntegerField()
    id_norme = models.ForeignKey(Norme, verbose_name="Normes", on_delete=models.CASCADE)
    id_chap=models.ForeignKey(Chapitre,verbose_name="Chapitres",on_delete=models.CASCADE)
    id_Sc1=models.ForeignKey(SC_niv1, verbose_name=("Sc_niv1"), on_delete=models.CASCADE,default=None, blank=True, null=True)
    id_Sc2=models.ForeignKey(SC_niv2, verbose_name=("Sc_niv2"), on_delete=models.CASCADE,default=None, blank=True, null=True)
    id_Sc3=models.ForeignKey(SC_niv3, verbose_name=("Sc_niv3"), on_delete=models.CASCADE,default=None, blank=True, null=True)
    id_point=models.ForeignKey(Point,verbose_name=("Points"),on_delete=models.CASCADE,default=None, blank=True, null=True)
    comment=models.TextField(default=None, blank=True, null=True)
    reponse=models.BooleanField()

    
class FileModel(models.Model):

    doc=models.FileField(upload_to=settings.MEDIA_ROOT)
    #uploaded= models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
    
        return str(self.doc)


class Notification(models.Model):
    id= models.AutoField(primary_key=True)
    type=models.IntegerField()
    date=models.DateField(default=timezone.now)
    vu=models.BooleanField(default=False)
    user=models.ForeignKey(User,verbose_name=("Users"),on_delete=models.CASCADE,default=None,blank=True, null=True)
    norme=models.ForeignKey(Norme,verbose_name=("Normes"),on_delete=models.CASCADE,default=None,blank=True, null=True)
    loi=models.ForeignKey(Loi,verbose_name=("Lois"),on_delete=models.CASCADE,default=None,blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
