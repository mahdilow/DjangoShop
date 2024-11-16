FROM python:3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN python -m pip install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

CMD [ "python","manage.py", "runserver","0.0.0.0:8000"]