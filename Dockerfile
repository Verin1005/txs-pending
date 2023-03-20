# FROM ubuntu:20.04
FROM browserless/chrome
# RUN apt update -y && apt-get install -y gnupg2 wget
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# ENV DEBIAN_FRONTEND=noninteractive
# ENV TZ=Europe/Berlin
# RUN apt install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils python3 python3-pip
# RUN apt install -y google-chrome-stable
USER root
RUN apt update -y && apt install -y python3 python3-pip
COPY . .
RUN pip install -r requirements.txt
# EXPOSE 3000
# CMD ["./start.sh && uvicorn main:app --host 0.0.0.0 --port 3000"]
