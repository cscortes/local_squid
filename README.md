# local squid
Running squid locally (on your PC or laptop)  makes running docker, web searching faster since rpms, images, files from the internet are cached locally.  The first 
time requested the web browser must hit the web.  
But after that, it will look to see if you have 
a local copy before trying the web.  

> Note: you need to configure things to know that 
> you are using a proxy.  Normally, these configurations
> are part of your settings of your web browser or 
> environmental variables before you run certain 
> programs.


## Pre-requisites

* Docker for Linux or Windows depending on your system
* Python if you are on Windows
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

    >  make run 

- To stop the server

    > make stop 

## Feel free to submit patches

If you find problems with code 
or have a great fix, submit an issue and 
include a patch if you can. 
