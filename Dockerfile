FROM debian:stable

ADD hello/requirements.txt /hello/requirements.txt

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get -y install python-pip curl && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp* && \
	pip install pip --upgrade && \
	pip install -r /hello/requirements.txt

ADD hello /hello

WORKDIR /hello/

EXPOSE 5000

CMD ["python", "manage.py", "runserver"]
