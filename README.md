# Local Squid

Running squid locally (on your PC or laptop)  makes running docker, web searching faster since rpms, images, files from the internet are cached locally.  

The first time requested the web browser must hit the web.  
But after that, it will look to see if you have 
a local copy before trying the web.  

> Note: you need to configure things to know that 
> you are using a proxy.  Normally, these configurations
> are part of your settings of your web browser or 
> environmental variables before you run certain 
> programs.

## Persistence

Even though it really is a choice, I've included a persistent
cache mechanism by using docker's volumes in the docker-compose.yaml. This way squid doesn't
have to start from scratch then next time you power up your machine.

```yaml
    volumes:
      - squidcache:/cache
```

## Port

The port being used for squid is 3128. Sometimes people select 8080 has their proxy port, but currently I was more focused on getting product out than allowing dev to change the port number.  

## Deployment

I have a fedora box, and a Windows 11 box.  If you have the prerequisites installed it should work.  I don't have a Mac so I can't test it on one.  I will be happy to add support if someone needs it and writes the code for it. 

## Resources

I've limited the docker-compose.yaml file to only use 2 cpus and 1G of memory.  I don't really thing it even uses that much ram ever.  But it is configurable:

```yaml
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: "1g"      
```

## Pre-requisites

* Docker for Linux or Windows depending on your system
* Python if you are on Windows, so you can run the make.py 
* 'make' if you are on Linux

## Running it on Windows

Even though it was written for a Fedora linux system, 
I also wanted it to run on Windows.

On a Windows system though, 
the 'make' utility doesn't exist
so I wrote the functionality I needed 
using AI (for fun), that is what the make.py does. 

If you want to run the makefile on a Windows system, 
you can download and install "python" for Windows.

- then in the project directory, type:

    > python make.py --list 

- for a List of targets in the make file. 

- Then build the squidserver locally (You only need to do this once on your system.  After that, as long as you don't delete your squidserver image you can skip this step).

    > python make.py build 

- Finally execute the squidserver locally with: 

    > python make.py run 

- To stop the server

    > python make.py stop 

## Running it on Linux


- Listing the targets:

    > cat Makefile | grep ":"

- build the squidserver locally (You only need to do this once on your system.  After that, as long as you don't delete your squidserver image you can skip this step).

    > make build 

- Finally execute the squidserver locally with: 

    >  make start

    or if you want to run it in background mode:
    
    > make bstart

- To stop the server

    > make stop 

- To run a quick test

    > make test 



## Feel free to submit patches

If you find problems with code or have a great fix, submit an issue and include a patch if you can. 

