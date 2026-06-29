FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip --quiet \
    && pip install pipenv --quiet \
    && pipenv requirements > requirements.txt \
    && pip install -r requirements.txt --quiet

COPY . .

CMD ["python", "-m", "gunicorn", "app:app", "--bind", "0.0.0.0:8000"]