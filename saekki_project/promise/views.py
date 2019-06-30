from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import PromiseForm
from .models import Friend, Promise

# index_page
def home(request):
    users = User.objects.exclude(id=request.user.id)
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()
    promises = Promise.objects.all()
    user = request.user

    return render(request, 'home.html', {'friends':friends, 'users':users, 'promises':promises, 'user':user})

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
    