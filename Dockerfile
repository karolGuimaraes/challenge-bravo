FROM python:3.5.2
ENV PYTHONHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /bravo
WORKDIR /bravo
COPY ./bravo /bravo

RUN adduser --disabled-password --gecos '' user
USER user