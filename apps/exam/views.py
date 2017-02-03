from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.db.models import Count
from datetime import datetime
from dateutil.parser import *
from django.db import connection


from ..LogReg.models import User
from .models import Quotes, Favorites

# Create your views here.

def index(request):
    user_id = request.session['logged_in_user']
    user = User.objects.get(id = request.session['logged_in_user'])
    y = Favorites.objects.filter(favorited_by=user).values('favorite__id')


    quotes = Quotes.objects.all().exclude(id__in=y)
    favorites = Favorites.objects.filter(favorited_by=user)

    context={
        'user': user,
        'quotes': quotes,
        'favorites': favorites,
    }

    return render(request, "exam/index.html", context)


def add(request):
    errors=[]
    flag = False
    if not request.POST['author']:
        errors.append("Quoted by is blank.")
        flag = True
    if not request.POST['quote']:
        errors.append("Message is blank.")
        flag = True
    if flag:
        for err in errors:
            messages.error(request, err)
        return redirect("/quotes")

    user = User.objects.get(id = request.session['logged_in_user'])
    author = request.POST['author']
    quote = request.POST['quote']
    Quotes.objects.create(quote=quote, author=author, poster=user)
    return redirect('/quotes')


def add_to_list(request, id):
    user = User.objects.get(id = request.session['logged_in_user'])
    quote = Quotes.objects.get(id=id)

    Favorites.objects.create(favorite=quote, favorited_by=user)

    return redirect('/quotes')


def remove_from_list(request, id):
    user = User.objects.get(id = request.session['logged_in_user'])
    quote = Quotes.objects.get(id=id)

    favorite_to_be_removed = Favorites.objects.filter(favorited_by=user).filter(favorite=quote)
    favorite_to_be_removed.delete()

    return redirect('/quotes')


def logout(request):
    auth.logout(request)
    return redirect("/main")


def users(request, id):
    person = User.objects.get(id=id)
    quotes = Quotes.objects.filter(poster=person)
    counting = Quotes.objects.filter(poster=person).count()

    context={
        'person': person,
        'counting': counting,
        'quotes': quotes,
    }
    return render(request, "exam/quotes.html", context)
