from django.http import JsonResponse

from .models import Norme, Chapitre, Point, Question_Generale
from django.shortcuts import render


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
    else:
        incr = int(p[taille - 2])
        incr = incr + 1
        incr=str(incr)
        id_chap = p[0] + "_" + incr
        if Chapitre.objects.filter(id_chap=id_chap).exists():
            id = "yes"
        else:
            quizz=""
            end=1

    data = {'quizz': quizz,
            'point': point_actu.titre,
            'point_descri':point_actu.point,
            'id':point_actu.id_point,
            'end':end
            }
    return JsonResponse(data)
