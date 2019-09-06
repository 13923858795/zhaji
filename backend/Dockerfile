FROM python:3.6-stretch

EXPOSE 5001

ENV ENV=production
ENV DEBUG=True
ENV MONGODB_HOST=mongo
ENV REDIS_URL=redis://redis
ENV SOCKET_HOST=0.0.0.0

COPY ./sources.list /etc/apt/sources.list

WORKDIR /app
RUN apt-get update 
RUN apt-get install -y libaio1 net-tools bc
RUN pip install -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com pipenv 
COPY Pipfile* /app/
RUN pipenv lock -r > requirements.txt
RUN pip install -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r requirements.txt
COPY . /app
RUN sh -c "echo /app/oracle/instantclient_18_5 > /etc/ld.so.conf.d/oracle-instantclient.conf" \
    && ldconfig
RUN export LD_LIBRARY_PATH=/app/oracle/instantclient_18_5:$LD_LIBRARY_PATH
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

CMD python run_pro.py

