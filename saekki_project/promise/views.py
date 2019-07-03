from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import PromiseForm
from .models import Friend, Promise, Party_detail

# index_page
def home(request):
    # 로그인 안된 상태
    if not request.user.is_authenticated:
        return redirect('login')
    # 로그인 되었을때
    else:
        users = User.objects.exclude(id=request.user.id)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        promises = Promise.objects.all()
        user = request.user
        
        return render(request, 'home.html', {'friends':friends, 'users':users, 'promises':promises, 'user':user})

# 디테일 보여주기
def detail(request, pk):
    promise = get_object_or_404(Promise ,pk=pk)

    return render(request, 'detail.html', {'promise':promise})


# 글쓰기
def new(request):
    if request.method == "POST":
        form = PromiseForm(request.POST)
        if form.is_valid():
            parties = request.POST.getlist('party_friend[]')
            promise = form.save(commit=False)
            promise.user = request.user
            promise.party = parties
            promise.latitude = float(request.POST['addr_lat'])
            promise.longitud = float(request.POST['addr_lng'])
            promise.save()

            # 참가자들의 성공여부를 저장하는 부분
            for party in parties:
                p = Party_detail()
                p.promise = promise
                p.user = User.objects.get(username=party)
                p.save()
            p = Party_detail()
            p.promise = promise
            p.user = request.user
            p.save()

            return redirect('home')
    else:
        form = PromiseForm()
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()

        return render(request, 'new.html', {'form':form, 'friends':friends})

# 친구추가, 해제 버튼
def change_friend(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
        Friend.make_friend(friend, request.user)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
        Friend.lose_friend(friend, request.user)

    return redirect('home')
    
# 도착이벤트
def arrived(request, promise_id):
    if request.method == 'POST':
        p = Party_detail.objects.get(promise=promise_id, user=request.user)
        p.success_or_fail = 1
        p.arrived_time = timezone.now()
        p.save()
        
        return redirect('home')
    else:
        return HttpResponse('오류')