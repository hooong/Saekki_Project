from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import *
from .models import *

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
        arrives = Party_detail.objects.filter(user=user, success_or_fail=1)
        no_arrives = Party_detail.objects.filter(user=user, success_or_fail=0)
        
        return render(request, 'home.html', {'friends':friends, 'users':users, 'promises':promises, 'user':user, 'arrives':arrives, 'no_arrives':no_arrives})

# 디테일 보여주기
def detail(request, pk):
    promise = get_object_or_404(Promise ,pk=pk)
    cur_user = request.user

    # 댓글
    comments = promise.comments.all()
    commentform = Promise_CommentForm()

    # 도착여부
    success = Party_detail.objects.get(promise=promise, user=request.user)

    return render(request, 'detail.html', {'promise':promise, 'comments':comments, 'commentform':commentform, 'success': success, 'cur_user':cur_user })

# 댓글작성
def new_comment(request, promise_id):
    if request.method == 'POST':
        form = Promise_CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.promise = Promise.objects.get(id=promise_id)
            comment.save()

            return redirect('/promise/detail/'+str(promise_id))

# 댓글 삭제
def com_del(request, promise_id, comment_id):
    promise = get_object_or_404(Promise, id=promise_id)
    comment = promise.comments.get(id=comment_id)
    comment.delete()

    return redirect('/promise/detail/'+str(promise_id))

# 글쓰기
def new(request):
    if request.method == "POST":
        form = PromiseForm(request.POST)
        if form.is_valid():
            parties = request.POST.getlist('party_friend[]')
            promise = form.save(commit=False)
            promise.setting_date_time = request.POST['pic_date']
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

# 약속 삭제
def pro_del(request, promise_id):
    promise = get_object_or_404(Promise ,id=promise_id)
    promise.delete()

    return redirect('home')

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
        promise = Promise.objects.get(id=promise_id)
        cur_lat = request.POST['current_lat']
        cur_lng = request.POST['current_lng']
        max_lat = float(promise.latitude) + 0.0006
        min_lat = float(promise.latitude) - 0.0006
        max_lng = float(promise.longitud) + 0.0006
        min_lng = float(promise.longitud) - 0.0006
        if cur_lat != '' and cur_lng != '':
            if (min_lat <= float(cur_lat) and float(cur_lat) <= max_lat) and (min_lng <= float(cur_lng) and float(cur_lng) <= max_lng):
                party = Party_detail.objects.get(promise=promise_id, user=request.user)
                party.success_or_fail = 1
                party.arrived_time = timezone.now()
                party.save()

                messages.info(request, '성공적으로 도착하셨습니다.')

                # 모두 도착했는지 확인
                party_all = promise.party_detail.all()
                arr = 0
                for party_arr in party_all:
                    if party_arr.success_or_fail == 1:
                        arr += 1
                if arr == len(party_all):
                    promise.end = 1
                    promise.save()

                return HttpResponseRedirect('/promise/detail/'+str(promise_id))
            else:
                messages.info(request, '아직 장소에 도착을 하지 못하셨습니다.')
                return HttpResponseRedirect('/promise/detail/'+str(promise_id))
        else:
            messages.info(request, '위치가 제대로 확인되지 않았습니다.')
            return HttpResponseRedirect('/promise/detail/'+str(promise_id))
    else:
        return HttpResponse('오류')