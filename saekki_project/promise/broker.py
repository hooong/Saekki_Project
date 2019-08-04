import time
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .models import *

# 스케쥴러 생성
def schedule():
    sched = BackgroundScheduler()
    sched.add_job(com_time, 'interval', seconds=60)
    sched.add_job(soon, 'interval', seconds=60)
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
            parties = Party_detail.objects.filter(promise=promise, success_or_fail=1)
            for party in parties:
                fun = Fun_Image.objects.filter(user=party)
                fun.delete()

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

# 시간 문자열 맞추기
def time_to_str(t):
    t = t.replace('-','')
    t = t.replace(':','')
    t = t.replace(' ','')
    if len(t) > 15:
        t = t[:14]

    return t

