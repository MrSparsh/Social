# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from userapp.forms import LoginForm, SearchForm, SignupForm, SetPasswordForm

URL = "http://127.0.0.1:8000/userapi/"


def index(request):
    return redirect("/login/")


def home(request):
    if 'action' in request.GET:
        request.session.flush()
        return redirect('/login/')

    if 'user' not in request.session.keys():
        return redirect('/login/')

    context = {
        "user": request.session["user"]
    }
    return render(request, 'userapp/home.html', context)



def users(request):
    if 'user' not in request.session.keys():
        return redirect('/login/')
    res = requests.get(URL)
    print(res.text)
    context = {
        "users": res.json()
    }
    return render(request, 'userapp/users.html', context)


def userpage(request, pk):
    if 'user' not in request.session.keys():
        return redirect('/login/')

    res = requests.get(URL+pk)
    context = {
        "user": res.json()
    }
    return render(request, 'userapp/userpage.html', context)


def login(request):
    if 'user' in request.session.keys():
        return redirect('/user/home/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_num = form.cleaned_data['phone_num']
            password = form.cleaned_data['password']
            print(form.cleaned_data)
            payload = {
                "phone_num": phone_num,
                "password": password,
            }
            res = requests.post(URL+'login/', data=payload)
            if res.status_code == 200:
                request.session['user'] = res.json()
                return redirect('user/home/')

    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, 'userapp/login.html', context)


def search(request):
    if 'user' not in request.session.keys():
        return redirect('/login/')

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            phone_num = form.cleaned_data['phone_num']
            print(form.cleaned_data)
            payload = {
                "phone_num": phone_num,
            }
            res = requests.get(URL + 'search/?phone_num=' + phone_num)
            if res.status_code == 200:
                context = {
                    "user": res.json()
                }
                return render(request, 'userapp/userpage.html', context)

    context = {
        "form": SearchForm()
    }
    return render(request, 'userapp/search.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            phone_num = form.cleaned_data['phone_num']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            payload = {
                "phone_num": phone_num,
                "email": email,
                "name": name,
                "id": id,
                "password": password
            }
            res = requests.post(URL, data=payload)
            if res.status_code == 200:
                request.session.flush()
                return redirect('/login/')
    context = {
        "form": SignupForm
    }
    return render(request, "userapp/signup.html", context)


def set_password(request):
    if 'user' not in request.session.keys():
        return redirect('/login/')

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            id = request.session["user"]["id"]
            password = form.cleaned_data['password']
            payload = {
                "password": password
            }
            res = requests.put(URL+id+'/', data=payload)
            if res.status_code == 200:
                return redirect('/login/')

    context = {
        "form": SetPasswordForm
    }
    return render(request, "userapp/set_password.html", context)