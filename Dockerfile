FROM python:3.7

RUN mkdir -p /home/app/
WORKDIR /home/app/

COPY . /home/app/

RUN bash requirements.sh

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
