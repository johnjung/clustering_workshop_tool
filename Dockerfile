FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app

RUN apt-get update
RUN apt-get install -y graphviz

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
