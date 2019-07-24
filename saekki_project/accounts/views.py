from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse
from promise.models import Friend
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        pro_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and pro_form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            profile = Profile.objects.create(user=request.user, image=request.FILES['image'])
            profile.save()
            Friend.objects.create(current_user=request.user)
            return redirect('home')
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')
    else:
        form = UserForm()
        pro_form = ProfileForm()
        return render(request, 'signup.html', {'form':form, 'pro_form':pro_form})

# mypage
def mypage(request):
    user = request.user

    return render(request, 'mypage.html', {"user":user})