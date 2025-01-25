from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import chromedriver_autoinstaller

# Django 설정 파일 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ateam.settings')

# Celery 앱 생성
app = Celery('ateam')

# Celery에 Django 설정 불러오기
app.config_from_object('django.conf:settings', namespace='CELERY')

# ChromeDriver를 Celery 워커 시작 전에 미리 설치
chromedriver_autoinstaller.install()

# Django 앱의 태스크 모듈 자동 탐지
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
