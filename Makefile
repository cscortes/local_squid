
PORT=3128
SVRHOST=127.0.0.1

info:
	docker images

build:
	@echo "Building the image called 'docsquid'"
	docker build . -t docsquid 

run:
	@echo "Running the image called 'docsquid' and named the container 'squidserver'"
	docker run  -p $(SVRHOST):$(PORT):$(PORT)/tcp -m 1G -h squidserver --rm --name squidserver docsquid 

stop:
	@echo "Stopping container 'squidserver'"
	docker stop -t 2 squidserver 

test:
	@echo "Setting squid server ..."
	curl -x "http://$(SVRHOST):$(PORT)" "https://google.com"
	@echo $@

scan:
	@echo "Scanning for squid server with nmap ..."
	nmap $(SVRHOST) -p 1025- | grep $(PORT)
