FROM python:3.10-slim

WORKDIR /entity-extraction

COPY . .

# RUN apt install -y postgresql

RUN pip install -r requirements.txt

# CMD ["flask", "--app", "test", "run"]
CMD ["python", "/entity-extraction/src/routes.py"]