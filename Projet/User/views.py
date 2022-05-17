
from .models import Norme, Chapitre, Point, Question_Generale

import codecs
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from pprint import pprint
from .models import FileModel
import csv
import os
from django.conf import settings


# Create your views here.


def index(request):
    normes=Norme.objects.all()
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




def csv(request):
    
    return render(request, 'testCSV.html', )



def upload(request):
    
    if request.method == "POST":

        file = request.FILES.get("file") 
        name=file.name
        fss = FileSystemStorage()
        filename = fss.save(name, file)
        url = fss.url(filename)
        FileModel.objects.create(doc=url)
        upload_data(request)
        #return JsonResponse({"link" : url})
        #return JsonResponse({'msg':'<span style="color: green;">File successfully uploaded</span>'})
        
    else :
        return  render(request, 'testCSV.html', )
   
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

