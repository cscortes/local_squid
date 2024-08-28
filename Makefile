info:
	docker images

build:
	docker build . -t docsquid 

run:
	/usr/bin/docker run  -p 127.0.0.1:3128:3128/tcp  --cpus='4' -m 1G -h squidserver --rm --name squidserver docsquid 


stop:
	/usr/bin/docker stop -t 2 squidserver 

test:
	nmap localhost -p 3000-
	curl -x "http://localhost:3128" "https://google.com"
	@echo $@
