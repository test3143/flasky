FROM python:3.6-alpine

ENV FLASK_APP myflix.py
ENV FLASK_CONFIG production

RUN adduser -D myflix
USER myflix

WORKDIR /home/myflix

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY myflix.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
