FROM python:alpine3.9

WORKDIR /app
COPY ./app /app

RUN pip3 install bs4

CMD ["python3", "get_win5.py"]