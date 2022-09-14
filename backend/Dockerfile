FROM python:3.8
WORKDIR /backend
COPY requirements.txt /backend
RUN apt-get clean && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential
RUN pip3 install --upgrade pip -r requirements.txt
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
COPY . /backend
EXPOSE 5000
