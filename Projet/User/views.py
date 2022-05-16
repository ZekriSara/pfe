import codecs
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from pprint import pprint
from .models import FileModel
import csv
import os
from django.conf import settings


# Create your views here.
def index(request):

    return render(request, "index.html")


def quizz(request):
    liste = ["chapitre", "descri chapitre", "point", "descri point", "question1", "question2", "question3"]
    context = {'liste': liste}
    print(dir(liste))
    return render(request, "quizz.html",context)

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
        for f in files:
            handle_uploaded_file(f)
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
