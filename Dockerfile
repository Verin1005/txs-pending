FROM docker.io/selenium/standalone-chrome
USER root
RUN apt update -y && apt install -y python3 python3-pip
EXPOSE 3000
COPY . /
RUN pip install -r /requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
