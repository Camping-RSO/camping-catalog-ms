FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt requirements.txt
COPY app /app
RUN pip install -r requirements.txt
