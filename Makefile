.PHONY: info build serve run start server stop test scan 

PORT=3128
SVRHOST=127.0.0.1
PROJECT_DIR=$(shell pwd)

info:
	docker images

build: docker-compose.yaml
	@echo "Building the image ..."
	docker compose build --pull

#Forground server
serve run start server: build 
	@echo "Running the image "
	docker compose up

stop:
	@echo "Stopping container ..."
	docker compose down

test:
	@echo "Setting squid server ..."
	curl -x "http://$(SVRHOST):$(PORT)" "https://google.com"
	@echo $@

scan:
	@echo "Scanning for squid server with nmap ..."
	nmap $(SVRHOST) -p 1025- | grep $(PORT)

deploy:
	echo -e '#!/bin/bash\n' > fedora/start.sh
	echo -e "cd $(PROJECT_DIR) && make server\n" >> fedora/start.sh
	echo -e '#!/bin/bash\n' > fedora/stop.sh
	echo -e "cd $(PROJECT_DIR) && make stop\n" >> fedora/stop.sh
	chmod 777 fedora/*.sh 
	sudo mv -f fedora/*.sh /usr/local/bin/