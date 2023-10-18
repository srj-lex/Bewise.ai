FROM python:3.9

WORKDIR /flask_project

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["/bin/bash", "run.sh"]