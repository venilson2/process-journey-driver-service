FROM python:3.7.17

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /app/files/tmp
RUN mkdir -p /app/files/images

RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]