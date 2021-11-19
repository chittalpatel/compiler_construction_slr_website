FROM python:3.8-slim-buster

RUN mkdir slr
COPY . /slr/
WORKDIR /slr
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python", "-u", "main.py" ]