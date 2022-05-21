
from .models import Norme, Chapitre, Point, Question_Generale, SC_niv1, SC_niv2,SC_niv3, Reponse

import codecs
from django.shortcuts import render
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



# Create your views here.


def index(request):

    normes=Norme.objects.all()
    chap=Chapitre.objects.all()
    point=Point.objects.all()
    qst= Question_Generale()
    for n in normes:
        n.delete()



    context={
        'normes':normes,
    }
    return render(request, "index.html",context)

def quizz(request,id):
    normes = Norme.objects.all()
    points = Point.objects.all()
    chapitres = Chapitre.objects.all()
    questions = Question_Generale.objects.all()
    i = len(questions)
    context = {
        'normes': normes,
        'chapitres': chapitres,
        'points': points,
        'questions': questions,
        'i': i,
    }

    return render(request, "quizz.html", context)

def resultat(request):
    return render(request,"result.html")

def maj2(request):
    x="essai"
    return JsonResponse({'x':x})



def maj(request):
######Récupération et incrémentation
    point_id = request.GET.get('point')
    p = point_id.split('_')
    taille = len(p)
    incr = int(p[taille - 1])
    incr = incr + 1
    incr = str(incr)
    id = ""
    for i in range(taille - 1):
        id = id + p[i] + "_"

    id = id + "0" + incr

########## Next point exists
    if Point.objects.filter(id_point=id).exists():
        end=0
        point_actu = Point.objects.get(id_point=id)
        questions = Question_Generale.objects.all()
        i=1
        quizz=""
        #code html pour les questions
        for q in questions:
            rep = ('<li>' +
                   '<div class="inline-block">' +
                   '<div class="question">' + q.question + '</div>' +
                   '<div class="check">' +
                   '<label> <input type="radio" id="' + q.id_qst + '_oui" name="choice-radio' + str(i) + '" value="' + point_actu.id_point + '/' + q.id_qst + '/oui"> Oui </label> &nbsp;&nbsp;' +
                   '<label> <input type="radio" id="' + q.id_qst + '_non" name="choice-radio' + str(i) + '" value="' + point_actu.id_point + '/' + q.id_qst + '/non"> Non </label>' +
                   '</div>' +
                   '<div class="comment">' +
                   '<input class="custom-search-input"  id="com' + str(i) + '" placeholder="com' + str(i) + '" >' +
                   '</div>' +
                   '</div>' +
                   '</li>')
            quizz = quizz+rep
            i=i+1
        data = {'quizz': quizz,
                'point': point_actu.titre,
                'point_descri': point_actu.point,
                'id': point_actu.id_point,
                'end': end
                }
    else:

        id_chap = "cis_01"
        if Chapitre.objects.filter(id_chap=id_chap).exists():
            end = 1
            data={"end":end}
            return JsonResponse(data)
        else:
            end = 2
            data = {"end": end}
            return JsonResponse(data)


    return JsonResponse(data)




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





@ensure_csrf_cookie
def upload_files(request):
    if request.method == "GET":
        return render(request, 'files_upload.html', )
    if request.method == 'POST':
        files = request.FILES.getlist('files[]', None)
        #print(files)
        #for f in files:
            #handle_uploaded_file(f)
        return JsonResponse({'msg':'<span style="color: green;">File successfully uploaded</span>'})
    else:
        return render(request, 'files_upload.html', )


def upload_data(request):

    text=open(os.path.join(settings.MEDIA_ROOT,'csv_test.csv'),'rb').read()
    print(text)
    for i,row in enumerate(text) :
            if i==0 :
                pass
            else :
                print(row)
                return render(request, 'files_upload.html', )


def upload_data2(request):
    obj=FileModel.objects.get()
    text=open(os.path.join(settings.MEDIA_ROOT,'csv_test.csv'),'rb').read()
    #print(text)
    khra=obj.doc.path
    khra2=khra.split('/')
    izan=khra2[2]
    print(khra)
    print('2')
    print(text)
    print(izan)
    with open(izan,'r') as f:
         reader=csv.DictReader(codecs.interdecode(f, "utf-8"),delimiter=";")

         for i,row in enumerate(reader) :
            if i==0 :
                pass
            else :
                print(row)
                return render(request, 'files_upload.html', )


def adminIndex(request):
    return render(request,'Admin/home/index.html')
def login(request):
    return render(request,"Admin/accounts/login.html")
def register(request):
    return render(request,"Admin/accounts/register.html")

def userindex(request):
    return render(request,"Admin/home/tables.html")
def ajouternorme(request):
    return render(request,"Admin/home/ajouternorme.html")