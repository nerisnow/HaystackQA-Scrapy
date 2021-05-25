FROM python:3.7.4-stretch
WORKDIR /app
# install as a package
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy code
COPY . /app

EXPOSE 8501

# cmd for running the API
CMD ["streamlit", "run", "app.py","--server.port","8501"]
