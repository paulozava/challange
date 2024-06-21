FROM python:3.11 as requirement

WORKDIR /tmp

RUN pip3 install pipenv

COPY Pipfile .

COPY Pipfile.lock .

RUN pipenv requirements > requirements.txt

FROM python:3.11

WORKDIR /app

COPY --from=requirement /tmp/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./app /app

EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--port", "8080"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
