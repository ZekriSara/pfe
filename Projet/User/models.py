from tkinter import CASCADE
from django.db import models

# Create your models here.


class Norme(models.Model):
    id=models.AutoField(primary_key=True,)
    titre=models.TextField()
    version=models.IntegerField()
    descriptif=models.TextField()

    class Meta:
        verbose_name_plural ="Normes"

    def __str__(self) -> str:
        
        return self.titre


class Chapitre(models.Model):
    num=models.AutoField(primary_key=True)
    id_chap=models.TextField()
    id_norme=models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    version=models.IntegerField()
    titre=models.IntegerField()
    descriptif=models.TextField()


    class Meta:
        verbose_name_plural ="Chapitres"

    def __str__(self) -> str:
        
        return self.titre

class SC_niv1(models.Model):
    num=models.AutoField(primary_key=True)
    id_norme=models.ForeignKey(Norme, verbose_name="Normes", on_delete=models.CASCADE)
    version=models.IntegerField()
    id_chap=models.ForeignKey(Chapitre,verbose_name="Chapitres",on_delete=models.CASCADE)
    id_Sc1=models.TextField()
    titre=models.IntegerField()
    objectif=models.TextField()

    class Meta:
        verbose_name_plural ="Sc_niv1"

    def __str__(self) -> str:
        
        return self.titre

class SC_niv2(models.Model):
    num=models.AutoField(primary_key=True)
    id_norme=models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    version=models.IntegerField()
    id_chap=models.ForeignKey(Chapitre,verbose_name="Chapitres",on_delete=models.CASCADE)
    id_Sc1=models.ForeignKey(SC_niv1, verbose_name=("Sc_niv1"), on_delete=models.CASCADE)
    id_Sc2=models.TextField()
    titre=models.IntegerField()
    objectif=models.TextField()

    class Meta:
        verbose_name_plural ="Sc_niv2"

    def __str__(self) -> str:
        
        return self.titre

class SC_niv3(models.Model):
    num=models.AutoField(primary_key=True)
    id_norme=models.ForeignKey(Norme, verbose_name=("Normes"), on_delete=models.CASCADE)
    version=models.IntegerField()
    id_chap=models.ForeignKey(Chapitre,verbose_name="Chapitres",on_delete=models.CASCADE)
    id_Sc1=models.ForeignKey(SC_niv1, verbose_name=("Sc_niv1"), on_delete=models.CASCADE)
    id_Sc2=models.ForeignKey(SC_niv2, verbose_name=("Sc_niv2"), on_delete=models.CASCADE)
    id_Sc3=models.TextField()
    titre=models.IntegerField()
    objectif=models.TextField()

    class Meta:
        verbose_name_plural ="Sc_niv3"

    def __str__(self) -> str:
        
        return self.titre

class Point(models.Model):
    id=models.AutoField(primary_key=True,)
    titre=models.TextField()
    version=models.IntegerField()
    descriptif=models.TextField()

    class Meta:
        verbose_name_plural ="Points"

    def __str__(self) -> str:
        
        return self.titre