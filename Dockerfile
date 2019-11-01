FROM python:3.7-buster

ARG DATABASE_URL
ARG APP_SETTINGS

VOLUME /app/static/tixte-games

WORKDIR /app
COPY . .

RUN pip install -r /app/requirements.txt

ENV APP_SETTINGS $APP_SETTINGS
ENV DATABASE_URL $DATABASE_URL
ENV PORT 80

EXPOSE 80

ENTRYPOINT ["sh", "run.sh"]