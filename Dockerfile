FROM python:3
# setup environment variable
ENV DockerHOME=/home/app/

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list
RUN apt-get install wget
RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-get install gnupg
RUN apt-key add linux_signing_key.pub
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/

# install dependencies
RUN pip install pipenv

# copy whole project to your docker home directory.
COPY . $DockerHOME

RUN pipenv sync

RUN pip install -r requirements.txt

RUN python3 manage.py migrate
# port where the Django app runs
EXPOSE 8000
# start server
CMD python3 manage.py runserver 0.0.0.0:8000