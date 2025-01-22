from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 기본 Django 설정을 Celery에 연결
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ateam.settings')

app = Celery('ateam')

# Celery는 기본적으로 'django'를 브로커로 사용하도록 설정합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 등록된 태스크들을 자동으로 발견
app.autodiscover_tasks()