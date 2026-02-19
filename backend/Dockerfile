FROM python:3.13
WORKDIR /app 

# install app deps (copy from ./requirements.txt and install and add/install to /app/requirements.txt in container)
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy src app (copy local ./app directory into /app/app inside the container)
COPY ./app /app/app

COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

# run backend and database migrations ('alembic ugrade head' is idempotent - it won't do anything if already at latest migration)
CMD ["sh", "-c", "alembic upgrade head && fastapi run app/main.py"]