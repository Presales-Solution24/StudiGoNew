# Dockerfile

# Install dependencies
FROM python:3.9-slim

WORKDIR /app

COPY . .

# RUN pip install --no-cache-dir -r requirements.txt

RUN pip config set global.timeout 100 && \
    pip config set global.retries 10 && \
    pip install --no-cache-dir -r requirements.txt

# Copy script wait-for-it
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV FLASK_APP=manage.py
# ENV FLASK_ENV=development

# Jalankan dengan menunggu mysql_db:3307
CMD ["/wait-for-it.sh", "mysql_db:3307", "--", "gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
