# docker build -t techexapi .
# docker run -d -p 5050:5000 techexapi
# docker exec -it a1411fdb7f70 /bin/bash  
FROM python:3.7.4

# install app dependencies
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# copy app
COPY ./dist /app
RUN unzip server.zip

EXPOSE 5000
CMD [ "./server", "--log_dir=./logs", "--postgres_host=172.17.0.1", "--postgres_port=25432"]
