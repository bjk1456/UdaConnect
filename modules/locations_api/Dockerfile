FROM python:3.7-alpine
RUN pip install --upgrade pip
WORKDIR .
RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev curl
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]