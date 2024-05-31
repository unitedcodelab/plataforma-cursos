FROM python:3.11.9-bullseye

WORKDIR /src

COPY requirements.txt .
COPY .env .
COPY ./src /src

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]