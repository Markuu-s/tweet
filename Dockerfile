FROM python:3.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY twitter.py /usr/src/app/
#COPY bot.py /usr/src/app/
COPY test.py /usr/src/app/
#COPY requirements.txt /usr/src/app/
#COPY chromedriver /usr/src/app/

#RUN pip3 freeze > requirements.txt
RUN pip3 install selenium
RUN pip3 install pytelegrambotapi
#RUN apt-get install -y chromium-browser

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/bin/

# set display port to avoid crash
ENV DISPLAY=:99

CMD ["python", "test.py"]