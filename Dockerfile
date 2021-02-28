FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

WORKDIR /usr/app

COPY requirements/base.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY ./ski .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
