FROM python:3.8.9-slim

WORKDIR /opt
COPY requirements.txt .
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install gcc -y
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "todolist.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]
