.PHONY: info build serve run start server stop test scan 

PORT=3128
SVRHOST=127.0.0.1

info:
	docker images

build: docker-compose.yaml
	@echo "Building the image ..."
	docker compose build --pull

serve run start server: build 
	@echo "Running the image "
	docker compose up -d 

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
