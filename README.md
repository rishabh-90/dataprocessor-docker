# dataprocessor-docker
Simple Data Processor built using Docker

Dataprocessor is checking for new feed after **Nth Minute** wich can be changed in the **Dockerfile of part1 cmd section** after filename third arugment is minutes with just number for eg: **CMD [ "python", "dataProcessor.py" ,"put the number here"]**

## Build Setup

``` bash
# Clone the repo
git clone https://github.com/rishabh-90/dataprocessor-docker.git

# navigate to project folder
cd <project-folder>

#Run the docker compose
docker-compose up

#To make changes to app and rebuild the docker
docker-compose up --build
