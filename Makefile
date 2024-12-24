.PHONY: info build serve run start server stop test scan bserve brun bstart bserver

PORT=3128
SVRHOST=127.0.0.1
PROJECT_DIR=$(shell pwd)
CURRENTUSER=$(shell whoami)

CONTAINER_LIST=docker container list --filter "name=local-squid"
DOCKER_LIST=docker images --filter "reference=local-squid-img"


info:
	@echo "===================================================================="
	@echo "Container:"
	@$(CONTAINER_LIST) | grep home-web || echo "No container Found!"
	@echo "-------------------------------------------------------------------"
	@echo "Images:"
	@$(DOCKER_LIST) | grep home-web || echo "No image Found!"
	@echo "-------------------------------------------------------------------"
	@echo "Mounts:"
	@echo "$(MOUNTS)"
	@echo "===================================================================="

build: docker-compose.yaml
	@echo "Building the image ..."
	docker compose build --pull

#Forground server
serve run start server: build 
	@echo "Running the image in Forground"
	docker compose up

#Forground server
bserve brun bstart bserver: build 
	@echo "Running the image in background"
	docker compose up -d 

run:
	docker compose exec -i cache-server bash 

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

clean: stop erase_drive
	@$(CONTAINER_LIST) -q | xargs -r docker rm -fv 
	@$(DOCKER_LIST) -q | xargs -r docker rmi 

erase_drive:
	@docker volume ls
	@docker volume rm local_squid_squidcache

create_scripts:
	echo -e '#!/bin/bash\n' > fedora/start.sh
	echo -e "cd $(PROJECT_DIR) && make server\n" >> fedora/start.sh
	echo -e '#!/bin/bash\n' > fedora/stop.sh
	echo -e "cd $(PROJECT_DIR) && make stop\n" >> fedora/stop.sh
	chmod 777 fedora/*.sh 
	sudo mv -f fedora/*.sh /usr/local/bin/

# this deploy is fedora specific
deploy: create_scripts
	sed 's/USER/$(CURRENTUSER)/g' ./fedora/docker-squid.service.template > ./fedora/docker-squid.service 
	chmod 600 fedora/*.service 
	sudo chown root:root fedora/*.service && sudo mv -f fedora/*.service /etc/systemd/system
	sudo /sbin/restorecon -v /etc/systemd/system/docker-squid.service 
	sudo systemctl enable docker-squid 
	sudo systemctl start docker-squid 