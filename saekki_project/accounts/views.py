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
        # pro_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['password']  == form.cleaned_data['password_check']:
                new_user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                # profile = Profile.objects.create(user=request.user, image=request.FILES['image'])
                # profile.save()
                Friend.objects.create(current_user=request.user)
                return redirect('home')
            else:
                return render(request, 'signup.html', {'form':form, 'error':'비밀번호와 비밀번호 확인이 다릅니다.'})
                # TODO: 이거 alert로 에러 내용 띄워주기.
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')
    else:
        form = UserForm()
        return render(request, 'signup.html', {'form':form})

# mypage
def mypage(request):
    user = request.user

    return render(request, 'mypage.html', {"user":user})

def mypage_modify(request):
    user = request.user

    return render(request, 'mypage_modify.html', {"user":user})

def mypage_mod_conf(request):
    if request.method == 'POST':
        user = request.user
        if user.socialaccount_set.all:
            Profile.objects.get_or_create(user=user)
        profile = Profile.objects.get(user=user)
        profile.state_msg = request.POST['msg']
        profile.save()
        return redirect('mypage')