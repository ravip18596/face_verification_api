FROM python:2.7-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV FLASK_ENV=production
#ENV VIRTUAL_ENV=/opt/venv
#RUN python -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY . /app/
RUN apt update && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN pip install --upgrade setuptools pip && pip install -r requirements.txt

EXPOSE 5000

CMD ["python","app.py"]