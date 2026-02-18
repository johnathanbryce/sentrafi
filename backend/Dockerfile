FROM python:3.13
WORKDIR /app 

# install app deps (copy from ./requirements.txt and install and add/install to /app/requirements.txt in container)
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy src app (copy local ./app directory into /app/app inside the container)
COPY ./app /app/app

# run backend
CMD ["fastapi", "run", "app/main.py"]