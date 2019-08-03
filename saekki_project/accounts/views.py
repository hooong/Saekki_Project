from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse
from promise.models import Friend
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from saekki_pro.settings import config_secret_common
import requests, json

User = get_user_model()

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

# 카톡로그인
def oauth(request):
    code = request.GET['code']

    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    access_token_request_uri += "client_id=" + str(client_id)
    access_token_request_uri += "&redirect_uri=" + str(redirect_uri)
    access_token_request_uri += "&code=" + code

    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']

    user_profile_info_uri = "https://kapi.kakao.com/v2/user/me?access_token="
    user_profile_info_uri += str(access_token)
    print(user_profile_info_uri)
    
    user_profile_info_uri_data = requests.get(user_profile_info_uri)
    user_json_data = user_profile_info_uri_data.json()
    user_id = user_json_data['id']
    nickname = user_json_data['properties']['nickname']
    profile_image = user_json_data['properties']['profile_image']
    thumbnail_image = user_json_data['properties']['thumbnail_image']

    # 카카오 회원가입
    if not User.objects.filter(uid=user_id):
        new_user = User.objects.create_user(user_id,nickname,'password')
        new_user.profile_image = profile_image
        new_user.thumbnail_image = thumbnail_image
        new_user.save()
        login(request, new_user)
    else:
        user = User.objects.get(uid=user_id)
        if user.profile_image != profile_image:
            user.profile_image = profile_image
            user.thumbnail_image = thumbnail_image
        login(request, user)

    return redirect('home')

def kakao(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'

    client_id = config_secret_common['kakao']['client_id']
    redirect_uri = 'http://127.0.0.1:8000/oauth'
    
    login_request_uri += 'client_id=' + str(client_id)
    login_request_uri += '&redirect_uri=' + str(redirect_uri)
    login_request_uri += '&response_type=code'

    request.session['client_id'] = client_id
    request.session['redirect_uri'] = redirect_uri

    return redirect(login_request_uri)