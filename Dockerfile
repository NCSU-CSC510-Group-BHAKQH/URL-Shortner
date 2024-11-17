FROM ubuntu/mysql

COPY docker/init.sql /tmp/init.sql

WORKDIR /url-shortner

COPY . /url-shortner

ENV MYSQL_ROOT_PASSWORD=admin123
ENV MYSQL_DATABASE=urlshortner

RUN apt-get update \ 
	&& apt-get -y install \
		libmysqlclient-dev \
		mysql-client \
		mysql-server \
		python3 \
		python3-pip

RUN pip3 install -r url_shortner_server/requirements.txt
RUN service mysql start && mysql -u root -padmin123 < /tmp/init.sql

EXPOSE 8000
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
