FROM python:3.8.5

COPY ./requirements.txt /usr/src/app/requirements.txt

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app

ENV FLASK_APP="wedding_list.py"
ENV FLASK_ENV="development"
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD [ "flask", "run" ]