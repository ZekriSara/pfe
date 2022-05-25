from datetime import datetime

from .models import Norme, Chapitre, Point, Question_Generale, SC_niv1, SC_niv2, SC_niv3, Reponse, Test

import codecs
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage, default_storage
from pprint import pprint
from .models import FileModel
import csv
import os
from django.conf import settings
import sys
import pandas as pd

# Auth side views

def login(request):
    return render(request,"Admin/accounts/login.html")
def register(request):
    return render(request,"Admin/accounts/register.html")

# Client side views


def index(request):

    normes=Norme.objects.all()
    tests=Test.objects.all()




    #for n in normes:
      #  n.delete()



    context={
        'normes':normes,
        'tests':tests
    }
    return render(request, "index.html",context)

def quizz(request,id):
    test= Test()
    test.id_norme= Norme.objects.get(id=id)
    test.finished= False
    test.date= datetime.now()
    test.save()

    test=str(test.id_test)
    link= "/quizz/"+id+"/"+test
    return redirect(link)

def quizz2(request,id, test):
    normes = Norme.objects.all()
    points = Point.objects.all()
    chapitres = Chapitre.objects.all()
    questions = Question_Generale.objects.all()
    i = len(questions)
    id= test



    t= Test.objects.get(id_test=id)

    if t.last_point == None:
        p = Point.objects.first()
    else:
        p= Point.objects.get(id_point=t.last_point)

    context = {
        'normes': normes,
        'chapitres': chapitres,
        'points': points,
        'questions': questions,
        'point':p,
        'i': i,
        'id_test':id
    }

    return render(request, "quizz.html", context)


def point_suivant(p):
    taille = len(p)
    incr = int(p[taille - 1])
    incr = incr + 1

    id = ""
    for i in range(taille - 1):
        id = id + p[i] + "_"
    if incr < 10:
        incr = str(incr)
        id = id + "0" + incr
    else:
        incr = str(incr)
        id = id + incr
    return id
def tailleMinus2(p):
    taille=len(p)
    incr = int(p[taille - 2])
    incr = incr + 1
    id = ""
    for i in range(taille - 2):
        id = id + p[i] + "_"

    if incr < 10:
        incr = str(incr)
        id = id + "0" + incr
    else:
        incr = str(incr)
        id = id + incr
    return id
def tailleMinus3(p):
    taille=len(p)
    incr = int(p[taille - 3])
    incr = incr + 1
    id = ""
    for i in range(taille - 3):
        id = id + p[i] + "_"

    if incr < 10:
        incr = str(incr)
        id = id + "0" + incr
    else:
        incr = str(incr)
        id = id + incr
    return id
def tailleMinus4(p):
    taille=len(p)
    incr = int(p[taille - 4])
    incr = incr + 1
    id = ""
    for i in range(taille - 4):
        id = id + p[i] + "_"

    if incr < 10:
        incr = str(incr)
        id = id + "0" + incr
    else:
        incr = str(incr)
        id = id + incr
    return id
def tailleMinus5(p):
    taille=len(p)
    incr = int(p[taille - 5])
    incr = incr + 1
    id = ""
    for i in range(taille - 5):
        id = id + p[i] + "_"

    if incr < 10:
        incr = str(incr)
        id = id + "0" + incr
    else:
        incr = str(incr)
        id = id + incr
    return id
def codeHtmlQuestion(point_actu):
    #conditionn si question existe sinon question generale
    i = 1
    quizz=""
    questions = Question_Generale.objects.filter(id_norme=point_actu.id_norme)
    for q in questions:
        rep = ('<li>' +
               '<div class="inline-block">' +
               '<div class="question">' + q.question + '</div>' +
               '<div class="check">' +
               '<label> <input type="radio" id="' + q.id_qst + '_oui" name="choice-radio' + str(
                    i) + '" value="' + point_actu.id_point + '/' + q.id_qst + '/oui"> Oui </label> &nbsp;&nbsp;' +
               '<label> <input type="radio" id="' + q.id_qst + '_non" name="choice-radio' + str(
                    i) + '" value="' + point_actu.id_point + '/' + q.id_qst + '/non"> Non </label>' +
               '</div>' +
               '<div class="comment">' +
               '<input class="custom-search-input"  id="com' + str(i) + '" placeholder="com' + str(i) + '" >' +
               '</div>' +
               '</div>' +
               '</li>')
        quizz = quizz + rep
        i = i + 1
    return quizz
def dataReturnNextChap(point_actu,end):
    quizz = codeHtmlQuestion(point_actu)
    id_chap= point_actu.id_chap.id_chap
    chap_actu = Chapitre.objects.get(id_chap=id_chap)
    if point_actu.id_Sc1 == None:
        data = {'quizz': quizz,
                'point': point_actu.titre,
                'point_descri': point_actu.point,
                'id': point_actu.id_point,
                'chap': chap_actu.titre,
                'chap_des': chap_actu.descriptif,
                'end': end,
                'cas': 4
                }
    else:
        if point_actu.id_Sc2 == None:
            sc1 = SC_niv1.objects.filter(id_Sc1=point_actu.id_Sc1.id_Sc1)
            data = {'quizz': quizz,
                    'point': point_actu.titre,
                    'point_descri': point_actu.point,
                    'id': point_actu.id_point,
                    'chap': chap_actu.titre,
                    'chap_des': chap_actu.descriptif,
                    'sc1': sc1.titre,
                    'sc1_des': sc1.objectif,
                    'end': end,
                    'cas': 4
                    }
        else:
            if point_actu.id_Sc3 == None:
                sc1 = SC_niv1.objects.filter(id_Sc1=point_actu.id_Sc1.id_Sc1)
                sc2 = SC_niv2.objects.filter(id_Sc2=point_actu.id_Sc2.id_Sc2)
                data = {'quizz': quizz,
                        'point': point_actu.titre,
                        'point_descri': point_actu.point,
                        'id': point_actu.id_point,
                        'chap': chap_actu.titre,
                        'chap_des': chap_actu.descriptif,
                        'sc1': sc1.titre,
                        'sc1_des': sc1.objectif,
                        'sc2': sc2.titre,
                        'sc2_des': sc2.objectif,
                        'end': end,
                        'cas': 4
                        }
            else:
                sc1 = SC_niv1.objects.filter(id_Sc1=point_actu.id_Sc1.id_Sc1)
                sc2 = SC_niv2.objects.filter(id_Sc2=point_actu.id_Sc2.id_Sc2)
                sc3 = SC_niv2.objects.filter(id_Sc3=point_actu.id_Sc3.id_Sc3)
                data = {'quizz': quizz,
                        'point': point_actu.titre,
                        'point_descri': point_actu.point,
                        'id': point_actu.id_point,
                        'chap': chap_actu.titre,
                        'chap_des': chap_actu.descriptif,
                        'sc1': sc1.titre,
                        'sc1_des': sc1.objectif,
                        'sc2': sc2.titre,
                        'sc2_des': sc2.objectif,
                        'sc3': sc3.titre,
                        'sc3_des': sc3.objectif,
                        'end': end,
                        'cas': 4
                        }

    return data
def dataReturnNextSC1(point_actu,end):

    if point_actu.id_Sc2 == None:
        sc1 = SC_niv1.objects.filter(id_Sc1=point_actu.id_Sc1.id_Sc1)
        data = {'quizz': quizz,
                'point': point_actu.titre,
                'point_descri': point_actu.point,
                'id': point_actu.id_point,
                'sc1': sc1.titre,
                'sc1_des': sc1.objectif,
                'end': end,
                'cas': 3
                }

    else:
        if point_actu.id_Sc3 == None:
            sc1 = SC_niv1.objects.filter(id_Sc1=point_actu.id_Sc1.id_Sc1)
            sc2 = SC_niv2.objects.filter(id_Sc2=point_actu.id_Sc2.id_Sc2)
            data = {'quizz': quizz,
                    'point': point_actu.titre,
                    'point_descri': point_actu.point,
                    'id': point_actu.id_point,
                    'sc1': sc1.titre,
                    'sc1_des': sc1.objectif,
                    'sc2': sc2.titre,
                    'sc2_des': sc2.objectif,
                    'end': end,
                    'cas': 3
                    }
        else:
            sc1 = SC_niv1.objects.filter(id_Sc1=point_actu.id_Sc1.id_Sc1)
            sc2 = SC_niv2.objects.filter(id_Sc2=point_actu.id_Sc2.id_Sc2)
            sc3 = SC_niv2.objects.filter(id_Sc3=point_actu.id_Sc3.id_Sc3)
            data = {'quizz': quizz,
                    'point': point_actu.titre,
                    'point_descri': point_actu.point,
                    'id': point_actu.id_point,
                    'sc1': sc1.titre,
                    'sc1_des': sc1.objectif,
                    'sc2': sc2.titre,
                    'sc2_des': sc2.objectif,
                    'sc3': sc3.titre,
                    'sc3_des': sc3.objectif,
                    'end': end,
                    'cas': 3
                    }

    return data
def dataReturnNextSC2(point_actu,end):

        if point_actu.id_Sc3 == None:
            sc2 = SC_niv2.objects.filter(id_Sc2=point_actu.id_Sc2.id_Sc2)
            data = {'quizz': quizz,
                    'point': point_actu.titre,
                    'point_descri': point_actu.point,
                    'id': point_actu.id_point,
                    'sc2': sc2.titre,
                    'sc2_des': sc2.objectif,
                    'end': end,
                    'cas': 2
                    }
        else:
            sc2 = SC_niv2.objects.filter(id_Sc2=point_actu.id_Sc2.id_Sc2)
            sc3 = SC_niv2.objects.filter(id_Sc3=point_actu.id_Sc3.id_Sc3)
            data = {'quizz': quizz,
                    'point': point_actu.titre,
                    'point_descri': point_actu.point,
                    'id': point_actu.id_point,
                    'sc2': sc2.titre,
                    'sc2_des': sc2.objectif,
                    'sc3': sc3.titre,
                    'sc3_des': sc3.objectif,
                    'end': end,
                    'cas': 2
                    }

        return data
def dataReturnNextSC3(point_actu,end):
    sc3 = SC_niv2.objects.filter(id_Sc3=point_actu.id_Sc3.id_Sc3)
    data = {'quizz': quizz,
            'point': point_actu.titre,
            'point_descri': point_actu.point,
            'id': point_actu.id_point,
            'sc3': sc3.titre,
            'sc3_des': sc3.objectif,
            'end': end,
            'cas': 1
            }
    return data
def maj(request):
    #sauvegarde de réponse
    rep= request.GET.get('rep')
    com=request.GET.get('com')
    point_id = request.GET.get('point')
    test= request.GET.get('test')

    pre = Point.objects.get(id_point=point_id)
    rep= rep.split(';')
    com= com.split(';')
    taille=len(rep)
    for i in range(taille):
        r= Reponse()
        incr= str(i+1)
        r.id_test= Test.objects.get(id_test= test)
        #id_qst= pre.id_norme + "_" + incr
        id_qst= str(i+1)
        r.id_qst = Question_Generale.objects.get(id_qst=id_qst)
        r.id_reponse=id_qst
        r.id_point= pre
        r.id_chap= pre.id_chap
        r.id_Sc1= pre.id_Sc1
        r.id_Sc2 = pre.id_Sc2
        r.id_Sc3 = pre.id_Sc3
        r.id_norme= Norme.objects.get(id=pre.id_norme.id)
        r.version = pre.version
        r.comment= com[i]
        if rep[i] == "oui":
            r.reponse= True
        else :
            r.reponse = False

        r.save()


    t= Test.objects.get(id_test=test)
    t.last_point= pre.id_point
    t.save()

#Récupération et incrémentation

    p = point_id.split('_')
    taille= len(p)
    id_point=point_suivant(p)
    end=0

# Next point exists
    if Point.objects.filter(id_point=id_point).exists():
        point_actu = Point.objects.get(id_point=id_point)
        quizz=codeHtmlQuestion(point_actu)
        data = {'quizz': quizz,
                'point': point_actu.titre,
                'point_descri': point_actu.point,
                'id': point_actu.id_point,
                'end': end,
                'cas':0
                }
    else: #NEXT SOUS CHAPITRE
        if taille== 6:
            id_sc3= tailleMinus2(p)
            if SC_niv3.objects.filter(id_Sc3=id_sc3).exists():
                point_actu = Point.objects.filter(id_Sc3=id_sc3,id_Sc2=pre.id_Sc2.id_Sc2,id_Sc1=pre.id_Sc1.id_Sc1, id_chap=pre.id_chap.id_chap).first()
                data = dataReturnNextSC3(point_actu, end)
                return JsonResponse(data)
            else:
                id_sc2= tailleMinus3(p)
                if SC_niv2.objects.filter(id_Sc2=id_sc2).exists():
                    point_actu = Point.objects.filter(id_Sc2=id_sc2, id_Sc1=pre.id_Sc1.id_Sc1,id_chap=pre.id_chap.id_chap).first()
                    data = dataReturnNextSC2(point_actu, end)
                    return JsonResponse(data)
                else:
                    id_sc1= tailleMinus4(p)
                    if SC_niv1.objects.filter(id_Sc1=id_sc1).exists():
                        point_actu = Point.objects.filter( id_Sc1=id_sc1, id_chap=pre.id_chap.id_chap).first()
                        data = dataReturnNextSC1(point_actu, end)
                        return JsonResponse(data)
                    else:
                        id_chap= tailleMinus5(p)
                        if Chapitre.objects.filter(id_chap=id_chap).exists():
                            point_actu = Point.objects.filter(id_chap=id_chap).first()
                            data = dataReturnNextChap(point_actu, end)
                            return JsonResponse(data)
                        else:
                            end = 1
                            #fin

        if taille== 5:
            id_sc2 = tailleMinus2(p)
            if SC_niv2.objects.filter(id_Sc2=id_sc2).exists():
                point_actu=Point.objects.filter(id_Sc2=id_sc2,id_Sc1=pre.id_Sc1.id_Sc1,id_chap=pre.id_chap.id_chap).first()
                data= dataReturnNextSC2(point_actu,end)
                return JsonResponse(data)
            else:
                id_sc1 = tailleMinus3(p)
                if SC_niv1.objects.filter(id_Sc1=id_sc1).exists():
                    point_actu = Point.objects.filter(id_Sc1=id_sc1, id_chap=pre.id_chap.id_chap).first()
                    data = dataReturnNextSC1(point_actu, end)
                    return JsonResponse(data)
                else:
                    id_chap = tailleMinus4(p)
                    if Chapitre.objects.filter(id_chap=id_chap).exists():
                        point_actu = Point.objects.filter(id_chap=id_chap).first()
                        data = dataReturnNextChap(point_actu, end)
                        return JsonResponse(data)
                    else:
                        end = 1
                        # fin

        if taille== 4:
            id_sc1= tailleMinus2(p)
            id_chap= pre.id_chap.id_chap
            if SC_niv1.objects.filter(id_Sc1=id_sc1).exists():
                point_actu = Point.objects.filter(id_chap=id_chap, id_sc1=id_sc1).first()
                data = dataReturnNextSC1(point_actu,end)
                return JsonResponse(data)
            else: #NEXT CHAPITRE
                id_chap= tailleMinus3(p)
                if Chapitre.objects.filter(id_chap=id_chap).exists():
                    point_actu=Point.objects.filter(id_chap=id_chap).first()
                    data= dataReturnNextChap(point_actu,end)
                    return JsonResponse(data)
                else:
                    #FIN
                    end=1


        if taille==3:
            id_chap = tailleMinus2(p)
            if Chapitre.objects.filter(id_chap=id_chap).exists():
                point_actu = Point.objects.filter(id_chap=id_chap).first()
                data= dataReturnNextChap(point_actu,end)
                return JsonResponse(data)

            else:
                return JsonResponse({'end':1})







    return JsonResponse(data)

def resultat(request):
    return render(request,"resultat.html")



# Admin side views



def adminIndex(request):
    return render(request,'Admin/home/index.html')

def userindex(request):
    return render(request,"Admin/home/tables.html")
def ajouternorme(request):
    return render(request,"Admin/home/ajouternorme.html")


def remplacer(file):
    newtext=""
    for char in file:
        newtext = newtext + char
    newtext=newtext.replace("Ã´","ô")
    newtext=newtext.replace("Ã©","é")
    newtext=newtext.replace("Ã¨", "è")
    newtext=newtext.replace("Ãª", "ê")
    newtext=newtext.replace("Ã»", "û")
    newtext=newtext.replace("Ã¹", "ù")
    newtext=newtext.replace("Ã§", "ç")
    newtext=newtext.replace("â€™", "'")

    newtext=newtext.replace("Ã","à")
    return newtext

def remplacer2(file):
    newtext=""
    for char in file:
        newtext = newtext + char
    newtext=newtext.replace("“","ô")
    newtext=newtext.replace("‚","é")
    newtext=newtext.replace("Š", "è")
    newtext=newtext.replace("ˆ", "ê")
    newtext=newtext.replace("Ã»", "û")
    newtext=newtext.replace("Ã¹", "ù")
    newtext=newtext.replace("Ã§", "ç")
    newtext=newtext.replace("?", "'")

    newtext=newtext.replace("Ã","à")
    return newtext

def upload(request):

    msg=1
    file = request.FILES.get("file")
    name = file.name
    fss = FileSystemStorage()
    filename = fss.save(name, file)
    url = fss.url(filename)

    FileModel.objects.create(doc=url)


    file = open(os.path.join(settings.MEDIA_ROOT, filename),'r').read()
    file= remplacer(file)

    #Récupération des valeurs de champ sasie
    id= request.POST.get("id")
    titre=request.POST.get("titre")
    desc=request.POST.get("desc")
    version=request.POST.get("version")


    #Remplissage de la base de données
    norme= Norme()
    norme.id=id
    norme.titre=titre
    norme.descriptif=desc
    norme.version=int(version)

    if Norme.objects.filter(id=id).exists():
        er="Cet identifiant existe, veuillez saisir un autre identifiant."
        return JsonResponse({"error": er,'msg':msg})
    else:
        norme.save()
        rows = file.split("\n")
        taille = len(rows)
        for i in range(1,taille):
            columns = rows[i-1].split(";")
            chap = Chapitre()
            chap.id_norme = norme
            chap.version = norme.version
            incr = str(i)
            if i<10:
                chap.id_chap = norme.id + "_0" + incr
            else:
                chap.id_chap = norme.id + "_" + incr
            chap.titre = columns[1]
            chap.descriptif = columns[2]
            chap.save()
        msg=0



    return JsonResponse({'msg':msg})

def upload2(request):
    nbFile=request.POST.get("nbFile")
    nbFile=int(nbFile)
    if (nbFile == 0):
        msg=0
        return JsonResponse({"msg":msg})
    if (nbFile >= 1):
        file1 = request.FILES.get("file1")
        name1 = file1.name
        fss = FileSystemStorage()
        filename1 = fss.save(name1, file1)
        url = fss.url(filename1)
        FileModel.objects.create(doc=url)
        file1 = open(os.path.join(settings.MEDIA_ROOT, filename1), 'r').read()
        file1 = remplacer(file1)
        rows1 = file1.split("\n")

        taille = len(rows1)
        for i in range(1, taille):
            souschap1 = SC_niv1()
            columns = rows1[i - 1].split(";")
            souschap1.id_chap = Chapitre.objects.get(id_chap=columns[0])
            souschap1.id_Sc1 = columns[1]
            souschap1.titre = columns[2]
            souschap1.objectif = columns[3]
            souschap1.id_norme = Norme.objects.get(id=columns[4])
            souschap1.version = columns[5]
            souschap1.save()


        if(nbFile >= 2):
            file2 = request.FILES.get("file2")
            name2 = file2.name
            fss = FileSystemStorage()
            filename2 = fss.save(name2, file2)
            url = fss.url(filename2)
            FileModel.objects.create(doc=url)

            file2 = open(os.path.join(settings.MEDIA_ROOT, filename2), 'r').read()
            file2 = remplacer(file2)
            rows2 = file2.split("\n")


            taille = len(rows2)
            for i in range(1, taille):
                souschap2 = SC_niv2()
                columns = rows2[i - 1].split(";")
                souschap2.id_chap = Chapitre.objects.get(id_chap=columns[0])
                souschap2.id_Sc1 = SC_niv1.objects.get(id_Sc1=columns[1])
                souschap2.id_Sc2=columns[2]
                souschap2.titre = columns[3]
                souschap2.objectif = columns[4]
                souschap2.id_norme = Norme.objects.get(id=columns[5])
                souschap2.version = columns[6]
                souschap2.save()

            if (nbFile == 3):
                file3 = request.FILES.get("file3")
                name3 = file3.name
                fss = FileSystemStorage()
                filename3 = fss.save(name3, file3)
                url = fss.url(filename3)
                FileModel.objects.create(doc=url)
                file3 = open(os.path.join(settings.MEDIA_ROOT, filename3), 'r').read()
                file3 = remplacer(file3)
                rows3 = file3.split("\n")

                taille = len(rows3)
                for i in range(1, taille):
                    souschap3 = SC_niv3()
                    columns = rows3[i - 1].split(";")
                    souschap3.id_chap = Chapitre.objects.get(id_chap=columns[0])
                    souschap3.id_Sc1 = SC_niv1.objects.get(id_Sc1=columns[1])
                    souschap3.id_Sc2 = SC_niv2.objects.get(id_Sc2=columns[2])
                    souschap3.id_Sc3 = columns[3]
                    souschap3.titre = columns[4]
                    souschap3.objectif = columns[5]
                    souschap3.id_norme = Norme.objects.get(id=columns[6])
                    souschap3.version = columns[7]
                    souschap3.save()


    return JsonResponse({"msg":0})

def upload3(request):

    file= request.FILES.get('file')
    file1= request.FILES.get('file1')
    name = file.name
    fss = FileSystemStorage()
    filename = fss.save(name, file)
    url = fss.url(filename)
    FileModel.objects.create(doc=url)

    file = open(os.path.join(settings.MEDIA_ROOT, filename), 'r').read()
    file = remplacer(file)
    rows = file.split("\n")
    taille = len(rows)

    for i in range(1, taille):

        point=Point()
        columns = rows[i - 1].split(";")


        if(len(columns) == 6):
            point.id_chap=Chapitre.objects.get(id_chap=columns[0])
            point.id_point=columns[1]
            point.titre=columns[2]
            point.point=columns[3]
            point.id_norme=Norme.objects.get(id=columns[4])
            point.version=columns[5]
            point.save()

        if(len(columns) == 7):
            point.id_chap=Chapitre.objects.get(id_chap=columns[0])
            if columns[1] == "":
                point.id_Sc1= None
            else:
                point.id_Sc1= SC_niv1.objects.get(id_Sc1=columns[1])
            point.id_point=columns[2]
            point.titre=columns[3]
            point.point=columns[4]
            point.id_norme=Norme.objects.get(id=columns[5])
            point.version=columns[6]
            point.save()

        if (len(columns) == 8):
            point.id_chap = Chapitre.objects.get(id_chap=columns[0])
            if columns[1] == "":
                point.id_Sc1 = None
            else:
                point.id_Sc1 = SC_niv1.objects.get(id_Sc1=columns[1])
            if columns[2] == "":
                point.id_Sc2 = None
            else:
                point.id_Sc2 = SC_niv2.objects.get(id_Sc2=columns[2])

            point.id_point = columns[3]
            point.titre = columns[4]
            point.point = columns[5]
            point.id_norme = Norme.objects.get(id=columns[6])
            point.version = columns[7]
            point.save()

        if (len(columns) == 9):
            point.id_chap = Chapitre.objects.get(id_chap=columns[0])
            if columns[1] == "":
                point.id_Sc1 = None
            else:
                point.id_Sc1 = SC_niv1.objects.get(id_Sc1=columns[1])
            if columns[2] == "":
                point.id_Sc2 = None
            else:
                point.id_Sc2 = SC_niv2.objects.get(id_Sc2=columns[2])
            if columns[3] == "":
                point.id_Sc3 = None
            else:
                point.id_Sc3 = SC_niv3.objects.get(id_Sc3=columns[3])
            point.id_point = columns[4]
            point.titre = columns[5]
            point.point = columns[6]
            point.id_norme = Norme.objects.get(id=columns[7])
            point.version = columns[8]
            point.save()


    name1 = file1.name
    fss = FileSystemStorage()
    filename1 = fss.save(name1, file1)
    url = fss.url(filename1)
    FileModel.objects.create(doc=url)
    file1 = open(os.path.join(settings.MEDIA_ROOT, filename1), 'r').read()
    file1 = remplacer(file1)
    rows1 = file1.split("\n")
    taille = len(rows1)

    columns1 = rows1[0].split(";")

    if len(columns1) == 3:
        for i in range(1, taille):
            columns1 = rows1[i-1].split(";")
            qst = Question_Generale()
            qst.id_qst = columns1[0]
            qst.id_norme = Norme.objects.get(id=columns1[1])
            qst.question = columns1[2]
            qst.save()


        ##remplissage qst generales

    #if len(columns) == 8:
        #remplissage qst



    msg=0
    return JsonResponse({"msg":msg})
