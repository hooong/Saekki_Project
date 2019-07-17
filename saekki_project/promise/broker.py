import time
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .models import *

# 스케쥴러 생성
def schedule():
    sched = BackgroundScheduler()
    sched.add_job(com_time, 'interval', seconds=60)
    # sched.add_job(all_arr, 'interval', seconds=60)
    sched.start()

# 시간 비교 후 끝났는지 확인
def com_time():
    print("스케쥴러 작동")
    promises = Promise.objects.all()
    for promise in promises:
        promise_date_time = time_to_str(promise.setting_date_time)
        now = time_to_str(str(timezone.now()))
        if now > promise_date_time:
            promise.end = 1
            promise.save()

# 시간 문자열 맞추기
def time_to_str(t):
    t = t.replace('-','')
    t = t.replace(':','')
    if len(t) > 15:
        t = t.replace(' ','')
        t = t[:14]
    else:
        t = t.replace('T','')
    
    return t

# 참가원이 모두 도착했는지 확인
def all_arr():
    print("모두도착했는가")
    promises = Promise.objects.all()
    for promise in promises:
        party_all = len(Party_detail.objects.get(promise=promise.id))
        party_arr = len(Party_detail.objects.get(promise=promise.id, success_or_fail=1))
        if party_all == party_arr:
            promise.end = 1
            promise.save()

    