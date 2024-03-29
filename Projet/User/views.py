import json
from datetime import datetime

from django.conf.global_settings import LOGIN_REDIRECT_URL
from django.conf.urls.static import static
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse

from .models import Norme, Chapitre, Point, Question, SC_niv1, SC_niv2, SC_niv3, Reponse, Test, Client, Loi, \
    Notification

import codecs
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
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

def log(request):
    return render(request, "Admin/accounts/login.html")


def register(request):
    return render(request, "Admin/accounts/register.html")


def khra(request):
    normes = Norme.objects.all()
    loi=Loi.objects.all()
    for l in loi:
        l.delete()
    for n in normes:
        n.delete()


    return render(request, "quizz.html")


@ensure_csrf_cookie
def reg(request):
    username = request.POST.get('username')
    entreprise = request.POST.get('entreprise')
    id_fisc = request.POST.get('id_fisc')
    email = request.POST.get('email')
    mdp = request.POST.get('mdp')
    err = 0

    if User.objects.filter(username=username).exists():
        err = 1
        erreur = "Ce Username est déjà utilisé."
        data = {
            'err': err,
            'erreur': erreur
        }
        return JsonResponse(data)

    if User.objects.filter(email=email).exists():
        err = 1
        erreur = "Cet email est déjà utilisé."
        data = {
            'err': err,
            'erreur': erreur
        }
        return JsonResponse(data)

    u = User()
    u.username = username
    u.email = email
    u.set_password(mdp)
    u.save()

    c = Client()
    c.id_user = u
    c.raison = entreprise
    c.num_fisc = id_fisc
    c.save()

    n=Notification()
    n.type=1
    n.user=u
    n.save()


    data = {
        'err': err,

    }

    return JsonResponse(data)


@ensure_csrf_cookie
def cnx(request):
    err = 0
    email = request.POST.get("email")
    mdp = request.POST.get("mdp")

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
       # hash = make_password(mdp)
        valid = user.check_password(mdp)
        if not valid:
            err = 1
            erreur = "Email ou mot de passe erronés"
            data = {
                "err": err,
                "erreur": erreur,
            }
            return JsonResponse(data)

        else:
            if user.is_active:
                login(request, user)
                request.session["user"] = user.username
                ad = user.is_superuser

                data = {
                    "err": err,
                    "ad": ad

                }
                return JsonResponse(data)
            else:
                err=1
                erreur= "Votre compte n'a pas encore été validé."
                data = {
                    "err": err,
                    "erreur": erreur,
                }
                return JsonResponse(data)


def ajouteradmin(request):
    notif = Notification.objects.filter(type=1).all()

    notif2 = Notification.objects.filter(type=1, vu=False).all()
    nb = len(notif2)

    context = {

        "notif": notif,
        "nb": nb
    }

    return render(request,"Admin/home/ajouteradmin.html",context)

def ajoutad(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    mdp = request.POST.get('mdp')
    err = 0

    if User.objects.filter(username=username).exists():
        err = 1
        erreur = "Ce Username est déjà utilisé."
        data = {
            'err': err,
            'erreur': erreur
        }
        return JsonResponse(data)

    if User.objects.filter(email=email).exists():
        err = 1
        erreur = "Cet email est déjà utilisé."
        data = {
            'err': err,
            'erreur': erreur
        }
        return JsonResponse(data)

    u = User()
    u.username = username
    u.email = email
    u.set_password(mdp)
    u.is_active = True
    u.is_superuser= True
    u.save()

    data = {
        'err': err,

    }

    return JsonResponse(data)

def listeadmins(request):

    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser is True:
            users=User.objects.filter(is_superuser=True).all()
            notif = Notification.objects.filter(type=1).all()

            notif2= Notification.objects.filter(type=1,vu=False).all()
            nb = len(notif2)

            context = {
                "users": users,
                "notif": notif,
                "nb": nb
            }
            return render(request, "Admin/home/admins.html", context)
        else:
            return redirect("/home/")

def deleteuser(request,id):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser is True:
            user = User.objects.filter(username=id).get()
            client = Client.objects.filter(id_user=user.id).get()
            client.is_valid = False
            client.save()
            return redirect("/users/")
        else:
            return redirect("/home/")



def deleteloi(request,id):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser is True:
            loi = Loi.objects.filter(id=id).get()
            loi.delete()
            return redirect("/lois/")
        else:
            return redirect("/home/")
def deletenorme(request,id):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser is True:
            loi = Norme.objects.filter(id=id).get()
            loi.delete()
            return redirect("/normes/")
        else:
            return redirect("/home/")

def voir(request,id):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser is True:

            notif = Notification.objects.get(id=id)
            notif.vu= True
            notif.save()

            return redirect("/users/")

        else:

            return redirect("/home/")



def valideruser(request, id):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser is True:
            user = User.objects.filter(username=id).get()
            user.is_active=True
            user.save()
            client= Client.objects.filter(id_user=user.id).get()
            client.is_valid= True
            client.save()
            return redirect("/users/")
        else:
            return redirect("/home/")


def logo(request):

    user=request.user
    logout(request)
    return redirect("/login/")

# Client side views

def index(request):

    if "user" not in request.session:
        return redirect('/login/')

    else:
        normes = Norme.objects.all()
        tests = Test.objects.filter(id_client=request.user.id).all()

        notif = Notification.objects.filter(type__in= (2,3)).all()
        notif2 = Notification.objects.filter(type__in=(2, 3),vu=False).all()
        nb = len(notif2)

        context = {
            'normes': normes,
            'tests': tests,
            'user': request.user,
            "notif": notif,
            "nb": nb
        }
        return render(request, "index.html", context)


def hist(request):


    if "user" not in request.session:

        return redirect('/login/')

    else:
        test = Test.objects.filter(id_client=request.user.id).all()
        notif = Notification.objects.filter(type__in= (2,3)).all()
        notif2 = Notification.objects.filter(type__in=(2, 3), vu=False).all()
        nb = len(notif2)
        context = {
            "test":test,
            "notif": notif,
            "nb": nb
        }
        return render(request, "history.html", context)

def normeuser(request):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        normes = Norme.objects.all()
        notif = Notification.objects.filter(type__in= (2,3)).all()
        notif2 = Notification.objects.filter(type__in=(2, 3), vu=False).all()
        nb = len(notif2)

        context = {
            "normes":normes,
            "notif": notif,
            "nb": nb
        }
        return render(request, "normes.html", context)


def voirnorme(request,id):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        notif= Notification.objects.get(id=id)
        notif.vu= True
        notif.save()
        return redirect('/norme/')

def voirloi(request,id):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        notif= Notification.objects.get(id=id)
        notif.vu= True
        notif.save()
        return redirect('/loi/')



def loiuser(request):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        lois = Loi.objects.all()
        notif = Notification.objects.filter(type__in= (2,3)).all()
        notif2 = Notification.objects.filter(type__in=(2, 3), vu=False).all()
        nb = len(notif2)

        context = {
            "lois": lois,
            "notif": notif,
            "nb": nb
        }
        return render(request, "lois.html", context)





def quizz(request, id):
    if "user" not in request.session:
        return redirect('/login/')
    else:
        test = Test()
        test.id_norme = Norme.objects.get(id=id)
        u = request.session["user"]
        test.id_client = User.objects.get(username=u)
        test.finished = False
        test.date = datetime.now()
        test.save()

        test = str(test.id_test)
        link = "/quizz/" + id + "/" + test

        if "user" not in request.session:
            return redirect('/login/')

        else:
            return redirect(link)




def quizz2(request, id, test):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        normes = Norme.objects.all()
        points = Point.objects.filter(id_norme=id)
        chapitres = Chapitre.objects.filter(id_norme=id)
        questions = Question.objects.filter(id_norme=id)
        i = len(questions)

        test=int(test)

        t = Test.objects.get(id_test=test)

        if t.last_point == None:
            p = Point.objects.filter(id_norme=id).first()
        else:
            p = Point.objects.get(id_point=t.last_point)

        notif = Notification.objects.filter(type__in= (2,3)).all()
        notif2 = Notification.objects.filter(type__in=(2, 3), vu=False).all()
        nb = len(notif2)




        context = {
            'normes': normes,
            'chapitres': chapitres,
            'points': points,
            'questions': questions,
            'point': p,
            'i': i,
            'id_test': test,
            "notif": notif,
            "nb": nb
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
    taille = len(p)
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
    taille = len(p)
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
    taille = len(p)
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
    taille = len(p)
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
    # conditionn si question existe sinon question generale
    i = 1
    quizz = ""
    questions = Question.objects.filter(id_norme=point_actu.id_norme)
    for q in questions:
        rep = ('<li>' +
               '<div class="inline-block">' +
               '<div class="question">' + q.question + '</div>' +
               '<div class="check">' +
               '<label> <input type="radio" id="' + q.id_qst + '_oui" name="choice-radio' + str(
                    i) + '" value="oui"> Oui </label> &nbsp;&nbsp;' +
               '<label> <input type="radio" id="' + q.id_qst + '_non" name="choice-radio' + str(
                    i) + '" value="non"> Non </label>' +
               '</div>' +
               '<div class="comment">' +
               '<input class="custom-search-input"  id="com' + str(i) + '" placeholder="com' + str(i) + '" >' +
               '</div>' +
               '</div>' +
               '</li>')
        quizz = quizz + rep
        i = i + 1
    return quizz


def dataReturnNextChap(point_actu, end,test,chapprec):
    quizz = codeHtmlQst(point_actu,test)
    id_chap = point_actu.id_chap.id_chap
    chap_actu = Chapitre.objects.get(id_chap=id_chap)
    if point_actu.id_Sc1 == None:
        data = {'quizz': quizz,
                'point': point_actu.titre,
                'point_descri': point_actu.point,
                'id': point_actu.id_point,
                'chap': chap_actu.titre,
                'chap_des': chap_actu.descriptif,
                'chapid':chap_actu.id_chap,
                'chapprec': chapprec.id_chap,
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


def dataReturnNextSC1(point_actu, end):
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


def dataReturnNextSC2(point_actu, end):
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


def dataReturnNextSC3(point_actu, end):
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

def pointPrec(point_actu):
    trouv=False

    points=Point.objects.filter(id_norme=point_actu.id_norme.id).all()
    point_prec=Point.objects.filter(id_norme=point_actu.id_norme.id).first()
    for p in points:
        if p.id_point == point_actu.id_point:
            trouv=True
        if trouv== False:
            point_prec=p

    return point_prec
def codeHtmlQst(point,test):
    i=1
    quizz=""
    questions = Question.objects.filter(id_norme=point.id_norme).all()
    if  Reponse.objects.filter(id_point=point.id_point, id_test=test).all():
        for q in questions:

            if Reponse.objects.filter(id_point=point.id_point, id_test=test, id_qst=q.id_qst).exists():
                rep = Reponse.objects.filter(id_point=point.id_point, id_test=test, id_qst=q.id_qst).get()
                if rep.reponse == True:
                    r = ('<li>' +
                         '<div class="inline-block">' +
                         '<div class="question">' + q.question + '</div>' +
                         '<div class="check">' +
                         '<label> <input type="radio" id="' + q.id_qst + '_oui" name="choice-radio' + str(
                                i) + '" value="oui" checked> Oui </label> &nbsp;&nbsp;' +
                         '<label> <input type="radio" id="' + q.id_qst + '_non" name="choice-radio' + str(
                                i) + '" value="non"> Non </label>' +
                         '</div>' +
                         '<div class="comment">' +
                         '<input class="custom-search-input"  id="com' + str(i) + '" placeholder="com' + str(
                                i) + '" >' +
                         '</div>' +
                         '</div>' +
                         '</li>')
                else:
                    r = ('<li>' +
                         '<div class="inline-block">' +
                         '<div class="question">' + q.question + '</div>' +
                         '<div class="check">' +
                         '<label> <input type="radio" id="' + q.id_qst + '_oui" name="choice-radio' + str(
                                i) + '" value="oui"> Oui </label> &nbsp;&nbsp;' +
                         '<label> <input type="radio" id="' + q.id_qst + '_non" name="choice-radio' + str(
                                i) + '" value="non" checked> Non </label>' +
                         '</div>' +
                         '<div class="comment">' +
                         '<input class="custom-search-input"  id="com' + str(i) + '" placeholder="com' + str(
                                i) + '" >' +
                         '</div>' +
                         '</div>' +
                         '</li>')
                quizz = quizz + r
                i = i + 1


        return quizz

    else:
        quizz = codeHtmlQuestion(point)
        return quizz


def prec(request):

    id_point=request.GET.get('point')
    id_test=request.GET.get('test')

    point_actu=Point.objects.get(id_point=id_point)

    point_prec=pointPrec(point_actu)
    #return JsonResponse({"msg":point_prec.id_point})
    test=Test.objects.get(id_test=id_test)

    quizz=codeHtmlQst(point_prec,test)

    data={
        'quizz': quizz,
        'point': point_prec.titre,
        'point_descri': point_prec.point,
        'id': point_prec.id_point,
        'chap': point_prec.id_chap.titre,
        'chap_des': point_prec.id_chap.descriptif,
        'chapprec':point_actu.id_chap.id_chap,
         'chapid': point_prec.id_chap.id_chap

    }

    return JsonResponse(data)



def maj(request):
    # sauvegarde de réponse
    rep = request.GET.get('rep')
    com = request.GET.get('com')
    point_id = request.GET.get('point')
    test = request.GET.get('test')

    pre = Point.objects.get(id_point=point_id)
    rep = rep.split(';')
    com = com.split(';')
    taille = len(rep)
    for i in range(taille):
        r = Reponse()
        incr = str(i + 1)
        r.id_test = Test.objects.get(id_test=test)
        id_qst= pre.id_norme.id + "_0" + incr
        r.id_qst = Question.objects.get(id_qst=id_qst)
        r.id_reponse = pre.id_point + "_0" + incr
        r.id_point = pre
        r.id_chap = pre.id_chap
        r.id_Sc1 = pre.id_Sc1
        r.id_Sc2 = pre.id_Sc2
        r.id_Sc3 = pre.id_Sc3
        r.id_norme = Norme.objects.get(id=pre.id_norme.id)
        r.version = pre.version
        r.comment = com[i]
        if rep[i] == "oui":
            r.reponse = True
        else:
            r.reponse = False

        r.save()

    t = Test.objects.get(id_test=test)
    t.last_point = pre.id_point
    t.save()

    # Récupération et incrémentation

    p = point_id.split('_')
    taille = len(p)
    id_point = point_suivant(p)
    end = 0

    # Next point exists
    if Point.objects.filter(id_point=id_point).exists():
        point_actu = Point.objects.get(id_point=id_point)
        quizz = codeHtmlQst(point_actu,test)
        data = {'quizz': quizz,
                'point': point_actu.titre,
                'point_descri': point_actu.point,
                'id': point_actu.id_point,
                'end': end,
                'cas': 0
                }
    else:  # NEXT SOUS CHAPITRE
        if taille == 6:
            id_sc3 = tailleMinus2(p)
            if SC_niv3.objects.filter(id_Sc3=id_sc3).exists():
                point_actu = Point.objects.filter(id_Sc3=id_sc3, id_Sc2=pre.id_Sc2.id_Sc2, id_Sc1=pre.id_Sc1.id_Sc1,
                                                  id_chap=pre.id_chap.id_chap).first()
                data = dataReturnNextSC3(point_actu, end)
                return JsonResponse(data)
            else:
                id_sc2 = tailleMinus3(p)
                if SC_niv2.objects.filter(id_Sc2=id_sc2).exists():
                    point_actu = Point.objects.filter(id_Sc2=id_sc2, id_Sc1=pre.id_Sc1.id_Sc1,
                                                      id_chap=pre.id_chap.id_chap).first()
                    data = dataReturnNextSC2(point_actu, end)
                    return JsonResponse(data)
                else:
                    id_sc1 = tailleMinus4(p)
                    if SC_niv1.objects.filter(id_Sc1=id_sc1).exists():
                        point_actu = Point.objects.filter(id_Sc1=id_sc1, id_chap=pre.id_chap.id_chap).first()
                        data = dataReturnNextSC1(point_actu, end)
                        return JsonResponse(data)
                    else:
                        id_chap = tailleMinus5(p)
                        if Chapitre.objects.filter(id_chap=id_chap).exists():
                            point_actu = Point.objects.filter(id_chap=id_chap).first()
                            data = dataReturnNextChap(point_actu, end,test, pre.id_chap)
                            return JsonResponse(data)
                        else:
                            end = 1
                            t = Test.objects.get(id_test=test)
                            t.finished = True
                            t.save()
                            # fin

        if taille == 5:
            id_sc2 = tailleMinus2(p)
            if SC_niv2.objects.filter(id_Sc2=id_sc2).exists():
                point_actu = Point.objects.filter(id_Sc2=id_sc2, id_Sc1=pre.id_Sc1.id_Sc1,
                                                  id_chap=pre.id_chap.id_chap).first()
                data = dataReturnNextSC2(point_actu, end)
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
                        data = dataReturnNextChap(point_actu, end,test, pre.id_chap)
                        return JsonResponse(data)
                    else:
                        end = 1
                        t = Test.objects.get(id_test=test)
                        t.finished = True
                        t.save()
                        # fin

        if taille == 4:
            id_sc1 = tailleMinus2(p)
            id_chap = pre.id_chap.id_chap
            if SC_niv1.objects.filter(id_Sc1=id_sc1).exists():
                point_actu = Point.objects.filter(id_chap=id_chap, id_sc1=id_sc1).first()
                data = dataReturnNextSC1(point_actu, end)
                return JsonResponse(data)
            else:  # NEXT CHAPITRE
                id_chap = tailleMinus3(p)
                if Chapitre.objects.filter(id_chap=id_chap).exists():
                    point_actu = Point.objects.filter(id_chap=id_chap).first()
                    data = dataReturnNextChap(point_actu, end,test, pre.id_chap)
                    return JsonResponse(data)
                else:
                    # FIN
                    end = 1
                    t = Test.objects.get(id_test=test)
                    t.finished = True
                    t.save()

        if taille == 3:
            id_chap = tailleMinus2(p)
            if Chapitre.objects.filter(id_chap=id_chap).exists():
                point_actu = Point.objects.filter(id_chap=id_chap).first()
                data = dataReturnNextChap(point_actu, end,test, pre.id_chap)
                return JsonResponse(data)

            else:
                t = Test.objects.get(id_test=test)
                t.finished= True
                t.save()
                return JsonResponse({'end': 1})




    return JsonResponse(data)


def resultat(request,id):
    if "user" not in request.session:
        return redirect('/login/')

    else:

        test = Test.objects.get(id_test=id)

        if test.finished == True:
            reponses = Reponse.objects.filter(id_test=test.id_test).all()
            comp = 0

            for r in reponses:
                if r.reponse == True:
                    comp = comp + 1

            pourcentage = (comp * 100) / len(reponses)

            labels = []
            values = []
            i = 1

            chapitres = Chapitre.objects.filter(id_norme=test.id_norme.id).all()

            for c in chapitres:
                smth = str(i)
                lab = "Chap" + smth
                labels.append(lab)
                comp = 0
                reponses = Reponse.objects.filter(id_chap=c.id_chap,id_test=id).all()
                for r in reponses:
                    if r.reponse == True:
                        comp = comp + 1

                val = (comp * 100) / len(reponses)
                values.append(val)

                i = i + 1

            labels.append("ok")
            val=90
            values.append(val)
            return render(request, "resultat.html",
                          context={"labels": json.dumps(labels),
                                   "values": json.dumps(values),
                                   "pourcent": pourcentage,
                                   "test":id,
                                   "norme": test.id_norme

                                   })


# Admin side views


def adminIndex(request):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser:
            client=Client.objects.all()
            test=Test.objects.all()
            norme=Test.objects.all()
            nbc=len(client)
            nbt=len(test)
            nbn=len(norme)

            notif=Notification.objects.filter(type=1).all()
            nb=len(notif)

            context={
                "nbc": nbc,
                "nbt": nbt,
                "nbn":nbn,
                "notif": notif,
                "nb": nb
            }
            return render(request, 'Admin/home/index.html',context)
        else:
            return redirect("/home/")


def userindex(request):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser is True:
            users=Client.objects.all()
            notif = Notification.objects.filter(type=1).all()
            notif2= Notification.objects.filter(type=1,vu=False).all()
            nb = len(notif2)

            context = {
                "users": users,
                "notif": notif,
                "nb": nb
            }
            return render(request, "Admin/home/tables.html", context)
        else:
            return redirect("/home/")


def ajouternorme(request):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user= User.objects.get(username=request.session["user"])

        if user.is_superuser:
            notif = Notification.objects.filter(type=1).all()

            notif2= Notification.objects.filter(type=1,vu=False).all()
            nb = len(notif2)

            context = {
                "notif": notif,
                "nb": nb
            }
            return render(request, "Admin/home/ajouternorme.html",context)
        else :
            return redirect("/home/")



def remplacer(file):
    newtext = ""
    for char in file:
        newtext = newtext + char
    newtext = newtext.replace("Ã´", "ô")
    newtext = newtext.replace("Ã©", "é")
    newtext = newtext.replace("Ã¨", "è")
    newtext = newtext.replace("Ãª", "ê")
    newtext = newtext.replace("Ã»", "û")
    newtext = newtext.replace("Ã¹", "ù")
    newtext = newtext.replace("Ã§", "ç")
    newtext = newtext.replace("â€™", "'")

    newtext = newtext.replace("Ã", "à")
    return newtext


def remplacer2(file):
    newtext = ""
    for char in file:
        newtext = newtext + char
    newtext = newtext.replace("“", "ô")
    newtext = newtext.replace("‚", "é")
    newtext = newtext.replace("Š", "è")
    newtext = newtext.replace("ˆ", "ê")
    newtext = newtext.replace("ƒ", "û")
    newtext = newtext.replace("–—", "ù")
    newtext = newtext.replace("‡", "ç")
    newtext = newtext.replace("?", "'")

    newtext = newtext.replace("…", "à")
    return newtext


def remplacer3(file):
    newtext = ""
    for char in file:
        newtext = newtext + char
    newtext = newtext.replace("™", "ô")
    newtext = newtext.replace("Ž", "é")
    newtext = newtext.replace("ž", "û")

    newtext = newtext.replace("ˆ", "à")
    return newtext


def codif(id, num):
    i = int(num)
    if i < 10:
        result = id + "_0" + num
    else:
        result = id + "_" + num
    return result


def upload(request):
    msg = 1
    file = request.FILES.get("file")
    name = file.name
    fss = FileSystemStorage()
    filename = fss.save(name, file)
    url = fss.url(filename)

    FileModel.objects.create(doc=url)

    path=settings.MEDIA_ROOT+"/csv"+"/"+filename

    file = open(os.path.join(settings.MEDIA_ROOT, filename), 'r', encoding='utf-8', errors='replace').read()
    file = remplacer(file)
    file = remplacer2(file)
    file = remplacer3(file)

    # Récupération des valeurs de champ sasie
    id = request.POST.get("id")
    titre = request.POST.get("titre")
    desc = request.POST.get("desc")
    version = request.POST.get("version")

    # Remplissage de la base de données
    norme = Norme()
    norme.id = id
    norme.titre = titre
    norme.descriptif = desc
    norme.version = int(version)

    if Norme.objects.filter(id=id).exists():
        er = "Cet identifiant existe, veuillez saisir un autre identifiant."
        return JsonResponse({"error": er, 'msg': msg})
    else:
        norme.save()
        rows = file.split("\n")
        taille = len(rows)
        columns = rows[0].split(";")
        if len(columns) != 3:
            er = "Ce fichier ne possède pas le nombre de colonnes nécessaire pour remplir la table des chapitres."
            return JsonResponse({"error": er, 'msg': msg})
        for i in range(1, taille):
            columns = rows[i - 1].split(";")
            chap = Chapitre()
            chap.id_norme = norme
            chap.version = norme.version
            num_chap = columns[0]
            chap.id_chap = codif(norme.id, num_chap)
            chap.titre = columns[1]
            chap.descriptif = columns[2]
            chap.save()
        msg = 0

    return JsonResponse({'msg': msg})


def upload2(request):
    nbFile = request.POST.get("nbFile")
    id = request.POST.get("id_norme")
    # return JsonResponse({"msg":1,"error":id})
    norme = Norme.objects.get(id=id)
    nbFile = int(nbFile)
    if (nbFile == 0):
        msg = 0
        return JsonResponse({"msg": msg})
    if (nbFile >= 1):
        file1 = request.FILES.get("file1")
        name1 = file1.name
        fss = FileSystemStorage()
        filename1 = fss.save(name1, file1)
        url = fss.url(filename1)
        FileModel.objects.create(doc=url)
        file1 = open(os.path.join(settings.MEDIA_ROOT, filename1), 'r').read()
        file = remplacer(file1)
        file = remplacer2(file)
        file1 = remplacer3(file)
        rows1 = file1.split("\n")

        taille = len(rows1)
        for i in range(1, taille):
            souschap1 = SC_niv1()
            columns = rows1[i - 1].split(";")
            id_chap = codif(norme.id, columns[0])
            souschap1.id_chap = Chapitre.objects.get(id_chap=id_chap)
            num_sc1 = columns[0]
            souschap1.id_Sc1 = codif(id_chap, num_sc1)
            souschap1.titre = columns[2]
            souschap1.objectif = columns[3]
            souschap1.id_norme = norme
            souschap1.version = norme.version
            souschap1.save()

        if (nbFile >= 2):
            file2 = request.FILES.get("file2")
            name2 = file2.name
            fss = FileSystemStorage()
            filename2 = fss.save(name2, file2)
            url = fss.url(filename2)
            FileModel.objects.create(doc=url)

            file2 = open(os.path.join(settings.MEDIA_ROOT, filename2), 'r').read()
            file = remplacer(file2)
            file = remplacer2(file)
            file2 = remplacer3(file)
            rows2 = file2.split("\n")

            taille = len(rows2)
            for i in range(1, taille):
                souschap2 = SC_niv2()
                columns = rows2[i - 1].split(";")
                id_chap = codif(norme.id, columns[0])
                souschap2.id_chap = Chapitre.objects.get(id_chap=id_chap)
                id_sc1 = codif(id_chap, columns[1])
                souschap2.id_Sc1 = SC_niv1.objects.get(id_Sc1=columns[1])
                id_sc2 = codif(id_sc1, columns[2])
                souschap2.id_Sc2 = id_sc2
                souschap2.titre = columns[3]
                souschap2.objectif = columns[4]
                souschap2.id_norme = norme
                souschap2.version = norme.version
                souschap2.save()

            if (nbFile == 3):
                file3 = request.FILES.get("file3")
                name3 = file3.name
                fss = FileSystemStorage()
                filename3 = fss.save(name3, file3)
                url = fss.url(filename3)
                FileModel.objects.create(doc=url)
                file3 = open(os.path.join(settings.MEDIA_ROOT, filename3), 'r').read()
                file = remplacer(file3)
                file = remplacer2(file)
                file3 = remplacer3(file)
                rows3 = file3.split("\n")

                taille = len(rows3)
                for i in range(1, taille):
                    souschap3 = SC_niv3()
                    columns = rows3[i - 1].split(";")
                    id_chap = codif(norme.id, columns[0])
                    souschap3.id_chap = Chapitre.objects.get(id_chap=id_chap)
                    id_sc1 = codif(id_chap, columns[1])
                    souschap3.id_Sc1 = SC_niv1.objects.get(id_Sc1=id_sc1)
                    id_sc2 = codif(id_sc1, columns[2])
                    souschap3.id_Sc2 = SC_niv2.objects.get(id_Sc2=id_sc2)
                    id_sc3 = codif(id_sc2, columns[3])
                    souschap3.id_Sc3 = id_sc3
                    souschap3.titre = columns[4]
                    souschap3.objectif = columns[5]
                    souschap3.id_norme = norme
                    souschap3.version = norme.version
                    souschap3.save()

    return JsonResponse({"msg": 0})


def upload3(request):
    id = request.POST.get("id_norme")
    norme = Norme.objects.get(id=id)

    file = request.FILES.get('file')
    file1 = request.FILES.get('file1')
    name = file.name
    fss = FileSystemStorage()
    filename = fss.save(name, file)
    url = fss.url(filename)
    FileModel.objects.create(doc=url)

    file = open(os.path.join(settings.MEDIA_ROOT, filename), 'r').read()
    file = remplacer(file)
    file = remplacer2(file)
    file = remplacer3(file)
    rows = file.split("\n")
    taille = len(rows)

    for i in range(1, taille):

        point = Point()
        columns = rows[i - 1].split(";")

        if (len(columns) == 4):
            id_chap = codif(norme.id, columns[0])
            point.id_chap = Chapitre.objects.get(id_chap=id_chap)
            id_point = codif(id_chap, columns[1])
            point.id_point = id_point
            point.titre = columns[2]
            point.point = columns[3]
            point.id_norme = norme
            point.version = norme.version
            point.save()

        if (len(columns) == 5):
            id_chap = codif(norme.id, columns[0])
            point.id_chap = Chapitre.objects.get(id_chap=id_chap)
            if columns[1] == "":
                point.id_Sc1 = None
                id_point = codif(id_chap, columns[2])
                point.id_point = id_point
            else:
                id_sc1 = codif(id_chap, columns[1])
                point.id_Sc1 = SC_niv1.objects.get(id_Sc1=id_sc1)
                id_point = codif(id_sc1, columns[2])
                point.id_point = id_point
            point.titre = columns[3]
            point.point = columns[4]
            point.id_norme = Norme.objects.get(id=columns[5])
            point.version = columns[6]
            point.save()

        if (len(columns) == 6):
            id_chap = codif(norme.id, columns[0])
            point.id_chap = Chapitre.objects.get(id_chap=id_chap)
            if columns[1] == "":
                point.id_Sc1 = None
                id_point = codif(id_chap, columns[3])
                point.id_point = id_point
            else:
                id_sc1 = codif(id_chap, columns[1])
                point.id_Sc1 = SC_niv1.objects.get(id_Sc1=id_sc1)
                if columns[2] == "":
                    point.id_Sc2 = None
                    id_point = codif(id_sc1, columns[3])
                    point.id_point = id_point
                else:
                    id_sc2 = codif(id_sc1, columns[2])
                    point.id_Sc2 = SC_niv2.objects.get(id_Sc2=id_sc2)
                    id_point = codif(id_sc2, columns[3])
                    point.id_point = id_point

            point.titre = columns[4]
            point.point = columns[5]
            point.id_norme = norme
            point.version = norme.version
            point.save()

        if (len(columns) == 7):
            id_chap = codif(norme.id, columns[0])
            point.id_chap = Chapitre.objects.get(id_chap=id_chap)
            if columns[1] == "":
                point.id_Sc1 = None
                id_point = codif(id_chap, columns[4])
                point.id_point = id_point
            else:
                id_sc1 = codif(id_chap, columns[1])
                point.id_Sc1 = SC_niv1.objects.get(id_Sc1=id_sc1)
                if columns[2] == "":
                    point.id_Sc2 = None
                    id_point = codif(id_sc1, columns[4])
                    point.id_point = id_point
                else:
                    id_sc2 = codif(id_sc1, columns[2])
                    point.id_Sc2 = SC_niv2.objects.get(id_Sc2=id_sc2)
                    if columns[3] == "":
                        point.id_Sc3 = None
                        id_point = codif(id_sc2, columns[4])
                        point.id_point = id_point
                    else:
                        id_sc3 = codif(id_sc2, columns[3])
                        point.id_Sc3 = SC_niv3.objects.get(id_Sc3=id_sc3)
                        id_point = codif(id_sc3, columns[4])
                        point.id_point = id_point

            point.titre = columns[5]
            point.point = columns[6]
            point.id_norme = norme
            point.version = norme.version
            point.save()

    name1 = file1.name
    fss = FileSystemStorage()
    filename1 = fss.save(name1, file1)
    url = fss.url(filename1)
    FileModel.objects.create(doc=url)
    file1 = open(os.path.join(settings.MEDIA_ROOT, filename1), 'r').read()
    file = remplacer(file1)
    file = remplacer2(file)
    file1 = remplacer3(file)
    rows1 = file1.split("\n")
    taille = len(rows1)

    for i in range(1, taille):
        columns1 = rows1[i - 1].split(";")
        if len(columns1) == 3:
            qst = Question()
            id_qst = codif(norme.id, columns1[0])
            qst.id_qst = id_qst
            qst.id_norme = norme
            qst.question = columns1[2]
            qst.version = norme.version
            qst.save()

        if (len(columns1) == 4):
            id_chap = codif(norme.id, columns1[0])
            id_point = codif(id_chap, columns1[1])
            id_qst = codif(id_point, columns1[2])
            qst = Question()
            qst.id_qst = id_qst
            qst.id_point = id_point
            qst.question = columns[4]
            qst.id_norme = norme
            qst.version = norme.version
            qst.save()

        if (len(columns1) == 5):

            id_chap = codif(norme.id, columns1[0])
            if columns[1] == "":
                id_point = codif(id_chap, columns1[2])
            else:
                id_sc1 = codif(id_chap, columns1[1])
                id_point = codif(id_sc1, columns1[2])

            id_qst = codif(id_point, columns1[3])
            qst = Question()
            qst.id_qst = id_qst
            qst.id_point = id_point
            qst.question = columns1[4]
            qst.id_norme = norme
            qst.version = norme.version
            qst.save()

        if (len(columns1) == 6):

            id_chap = codif(norme.id, columns1[0])
            if columns1[1] == "":
                id_point = codif(id_chap, columns1[3])
            else:
                id_sc1 = codif(id_chap, columns1[1])
                if columns1[2] == "":
                    id_point = codif(id_sc1, columns1[3])
                else:
                    id_sc2 = codif(id_sc1, columns1[2])
                    id_point = codif(id_sc2, columns1[3])

            id_qst = codif(id_point, columns1[4])
            qst = Question()
            qst.id_qst = id_qst
            qst.id_point = id_point
            qst.question = columns1[4]
            qst.id_norme = norme
            qst.version = norme.version
            qst.save()

        if (len(columns1) == 7):

            id_chap = codif(norme.id, columns1[0])
            if columns1[1] == "":
                id_point = codif(id_chap, columns1[4])
            else:
                id_sc1 = codif(id_chap, columns1[1])
                if columns1[2] == "":
                    id_point = codif(id_sc1, columns1[4])
                else:
                    id_sc2 = codif(id_sc1, columns1[2])
                    if columns1[3] == "":
                        id_point = codif(id_sc2, columns1[4])
                    else:
                        id_sc3 = codif(id_sc2, columns1[3])
                        id_point = codif(id_sc3, columns1[4])

            id_qst = codif(id_point, columns1[5])
            qst = Question()
            qst.id_qst = id_qst
            qst.id_point = id_point
            qst.question = columns1[4]
            qst.id_norme = norme
            qst.version = norme.version
            qst.save()

            n= Notification()
            n.type=2
            n.norme=norme
            n.save()

    msg = 0
    return JsonResponse({"msg": msg})

def indexloi(request):

    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser:
            notif = Notification.objects.filter(type=1).all()

            notif2= Notification.objects.filter(type=1,vu=False).all()
            nb = len(notif2)

            context = {
                "notif": notif,
                "nb": nb
            }
            return render(request, "Admin/home/ajouterloi.html",context)
        else:
            return redirect("/home/")



def ajouterloi(request):
    id=request.POST.get("id")
    titre=request.POST.get("titre")
    desc=request.POST.get("desc")
    file = request.FILES.get("file")




    if Loi.objects.filter(id=id).exists():
        msg="Cet identifiant de loi existe déjà"
        return JsonResponse({
            'error':msg,
            'msg':1

        })
    loi= Loi()
    loi.id=id
    loi.titre=titre
    loi.descriptif=desc
    loi.file_name=File(file, file.name)
    loi.save()

    n= Notification()
    n.type=3
    n.loi=loi
    n.save()

    data={
        "msg": 0

    }
    return JsonResponse(data)

def normes(request):
    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser:
            normes=Norme.objects.all()
            notif = Notification.objects.filter(type=1).all()

            notif2= Notification.objects.filter(type=1,vu=False).all()
            nb = len(notif2)

            context = {
                "normes":normes,
                "notif": notif,
                "nb": nb
            }
            return render(request,"Admin/home/normes.html", context)
        else:
            return redirect('/home/')

def lois(request):

    if "user" not in request.session:
        return redirect('/login/')

    else:
        user = User.objects.get(username=request.session["user"])
        if user.is_superuser:
            lois=Loi.objects.all()
            notif = Notification.objects.filter(type=1).all()

            notif2= Notification.objects.filter(type=1,vu=False).all()
            nb = len(notif2)

            context = {
                "lois":lois,
                "notif": notif,
                "nb": nb
            }
            return render(request,"Admin/home/lois.html", context)
        else:
            return redirect('/home/')