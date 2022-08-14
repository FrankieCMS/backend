FROM python:3.10

WORKDIR /srv/app
COPY ../requirements.txt /srv/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app/app /srv/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


