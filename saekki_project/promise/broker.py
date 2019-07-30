import time
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .models import *

# 스케쥴러 생성
def schedule():
    sched = BackgroundScheduler()
    sched.add_job(com_time, 'interval', seconds=60)
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
    t = t.replace(' ','')
    if len(t) > 15:
        t = t[:14]
        
    return t