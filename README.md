# CodeXpose
[![Build Status](https://travis-ci.org/Imaginea/codeXpose.svg?branch=master)](https://travis-ci.org/Imaginea/codeXpose)
[![Coverage Status](https://coveralls.io/repos/github/Imaginea/codeXpose/badge.svg?branch=master)](https://coveralls.io/github/Imaginea/codeXpose?branch=master)</br>
An open source one-stop solution for conducting technical interviews.

# Tech stack
Backened  - Python / Django<br>
Frontend - React/Redux<br>
Ops - Ansible/Docker/Nginx

# Architecture 
![alt text](https://github.com/inovizz/codeXpose/blob/master/architecturediagram.png?raw=true)
<sup>Please note, "Docker" and its logo are trademarks of Docker Inc.</sup>

# Getting Started
Follow the below steps to get the development environment up and running.

### Clone the repo
`$ git clone https://github.com/inovizz/codeXpose.git`<br>
`$ cd codeXpose`<br>

## Using Ansible 
### Install Ansible
`$ sudo apt-add-repository ppa:ansible/ansible`<br>
`$ sudo apt-get update`<br>

`$ sudo apt-get install ansible`<br>

### Execute the following playbook and shell script
`$ ansible-playbook deploy.yml -K`<br>
`$ . run_server.sh`<br>

Now, the server should be running at - <br>
`http://127.0.0.1:8000/`

To run the server using gunicorn and Nginx:<br>
`$ ./start_gunicorn.sh`

Now, the server should be running at - <br>
`http://localhost/`

To stop the gunicorn server:<br>
`$ sudo fuser -k 8000/tcp`

Note the default admin user is **admin@xyz.com**<br>


## Using Docker
### Install Docker and Docker Compose
`wget -qO- https://get.docker.com/ | sh`<br>
`sudo apt-get -y install python-pip`<br>
`sudo pip install docker-compose`<br>

Once docker and docker-compose are installed w/o any errors then run following command - 

`docker-compose up`

Post this, your django dev server shall be up and running at - <br>
`http://127.0.0.1:8000/`

### Create superuser
`docker ps` #find the container id<br>
`docker exec -ti [container id] bash`<br><br>
Above command takes you inside the docker container and code is available at /src directory, please refer to the django documentation and create a superuser for you.<br>
*Note: Currently, we are facing issues with docker setup. [Issue#56](https://github.com/Imaginea/codeXpose/issues/56) has been raised to address the same.*<br>

# Contributing
Please see [contribution](CONTRIBUTING.md).
