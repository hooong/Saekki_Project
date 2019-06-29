from django.shortcuts import render, redirect
from .forms import UserForm
from django.http import HttpResponse
from promise.models import Friend
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            Friend.objects.create(current_user=request.user)
            return redirect('home')
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')
    else:
        form = UserForm()
        return render(request, 'signup.html', {'form':form})