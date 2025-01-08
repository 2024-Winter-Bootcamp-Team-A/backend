FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1

# Python 로그가 버퍼링 없이 출력
ENV PYTHONUNBUFFERED 1

WORKDIR /Backend

# 필요한 파일 복사
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# 소스 코드 복사
COPY . ./

# 프로젝트 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]