from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")


def quizz(request):
    return render(request, "quizz.html")
