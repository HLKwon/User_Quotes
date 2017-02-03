from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import re
import bcrypt


def index(request):

    return render(request, "LogReg/index.html")



def register(request):


    postData = {
        'name': request.POST['name'],
        'alias': request.POST['alias'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'cPassword': request.POST['cPassword'],
        'birthday': request.POST['birthday'],
    }

    results = User.objects.rValidate(postData)
    #(True, [err err err])
    #(False, user obj)
    if results[0]: #if flag is True i.e. there is an error
        for err in results[1]: #taking string messages in list error from Models.py
                                #and then repackage them into messages list below
            messages.error(request, err) #django framework messages

    else:
        request.session['logged_in_user'] = results[1].id
        return redirect("/quotes")


    return redirect("/main")



def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }

    results = User.objects.lValidate(postData)


    if results[0]:
        request.session['logged_in_user'] = results[1].id

        return redirect("/quotes")

    else:
        messages.error(request, results[1])
        return redirect("/main")
