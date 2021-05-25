FROM python:3.7.4-stretch

WORKDIR /app

# install as a package
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy code
COPY . .

EXPOSE 5000

# cmd for running the API
CMD sleep 60 && python index.py && gunicorn -b :5000 app:app
