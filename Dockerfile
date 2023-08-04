FROM python:3.10-slim

COPY ./apps /app/apps
COPY ./requirements.txt /app
COPY ./.env /app
COPY apps/static /app/apps/

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8086

CMD ["uvicorn", "--factory", "apps.application:get_app", "--host=0.0.0.0", "--port", "8086",  "--reload"]
