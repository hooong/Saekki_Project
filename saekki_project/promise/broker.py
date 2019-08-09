import time
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .models import *
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

# 스케쥴러 생성
def schedule():
    sched = BackgroundScheduler()
    sched.add_job(com_time, 'cron', minute='*' ,second=1)
    sched.add_job(soon, 'cron', minute='*' ,second=30)
    sched.add_job(noti_count_penalty, 'cron', minute='*' ,second=55)
    sched.start()

# 시간 비교 후 끝났는지 확인
def com_time():
    print("끝난약속 잡기")
    promises = Promise.objects.all()
    for promise in promises:
        promise_date_time = time_to_str(promise.setting_date_time)
        now = time_to_str(str(timezone.now()))
        if now > promise_date_time:
            promise.end = 1
            promise.save()

        # 도착한 사람들 엽사 삭제
        if promise.what_betting == '엽사' and promise.end == 1:
            parties = Party_detail.objects.filter(promise=promise, success_or_fail=1)
            for party in parties:
                fun = Fun_Image.objects.filter(user=party)
                fun.delete()
            
            # 엽사 공개 알림
            parties = Party_detail.objects.filter(promise=promise, success_or_fail=0, acpt=1)
            for uid in parties:
                user = User.objects.get(uid=uid.user.uid)
                noti = Notification_penalty.objects.get_or_create(user=user, promise=promise)
                if noti[1]:
                    noti[0].penalty = '-1'
                    noti[0].save()
        
        # 벌금 알림 생성
        if promise.what_betting == '벌금' and promise.end == 1:
            parties = Party_detail.objects.filter(promise=promise, success_or_fail=0, acpt=1)
            for uid in parties:
                user = User.objects.get(uid=uid.user.uid)
                noti = Notification_penalty.objects.get_or_create(user=user, promise=promise)
                if noti[1]:
                    if promise.per_or_one == '시간':
                        uid.penalty = promise.per_min_money
                        uid.save()
                        noti[0].penalty = promise.per_min_money
                        noti[0].save()
                    elif promise.per_or_one == '한번':
                        uid.penalty = promise.onetime_panalty
                        uid.save()
                        noti[0].penalty = promise.onetime_panalty
                        noti[0].save()

# 마감 알려주기
def soon():
    print("마감임박!")
    promises = Promise.objects.all().exclude(end=1)
    for promise in promises:
        promise_date_time = time_to_str(promise.setting_date_time)
        now = time_to_str(str(timezone.now()))
        soon_time = int(promise_date_time) - int(now)
        # 1시간도 안남음
        if soon_time < 10000:
            promise.soon = str(1)
            promise.save()
        # 2시간도 안남음    
        elif soon_time < 20000:
            promise.soon = str(2)
            promise.save()
        # 3시간도 안남음    
        elif soon_time < 30000:
            promise.soon = str(3)
            promise.save()
        # 4시간도 안남음    
        elif soon_time < 40000:
            promise.soon = str(4)
            promise.save()
        # 5시간도 안남음    
        elif soon_time < 50000:
            promise.soon = str(5)
            promise.save()
        # TODO: 알림도 만들어주기.

# 알림 벌금계산
def noti_count_penalty():
    print("벌금 최신화")
    promises = Promise.objects.filter(end=1, what_betting='벌금', per_or_one='시간')
    for promise in promises:
        noties = Notification_penalty.objects.filter(promise=promise, final='0')
        for noti in noties:
            now = datetime.now()
            s = promise.setting_date_time
            set_time = datetime(int(s[:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:]))
            diff_time = ((now-set_time).seconds / 60)
            diff_time = int(diff_time) // int(promise.setting_min)
            penalty = str(int(promise.per_min_money)*(1 + diff_time))
            p = Party_detail.objects.get(user=noti.user, promise=promise)
            p.penalty = penalty
            p.save()
            noti.penalty = penalty
            noti.save()

# 시간 문자열 맞추기
def time_to_str(t):
    t = t.replace('-','')
    t = t.replace(':','')
    t = t.replace(' ','')
    if len(t) > 15:
        t = t[:14]

    return t



