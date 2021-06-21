FROM python:3.8-alpine
RUN apk update && apk add make
RUN mkdir -p home/app
COPY . /home/app
WORKDIR /home/app
RUN pip install -r requirements.txt
EXPOSE 8000
RUN make refresh_db
CMD ["make", "start"]
