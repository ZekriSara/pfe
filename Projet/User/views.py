from django.shortcuts import render


# Create your views here.
def index(request):

    return render(request, "index.html")


def quizz(request):
    liste = ["chapitre", "descri chapitre", "point", "descri point", "question1", "question2", "question3"]
    context = {'liste': liste}
    print(dir(liste))
    return render(request, "quizz.html",context)
