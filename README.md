# dataprocessor-docker
Simple Data Processor built using Docker

Dataprocessor is checking for new feed after **Nth Minute** wich can be changed in the **Dockerfile of part1 cmd section** after filename third arugment is minutes with just number for eg: **CMD [ "python", "dataProcessor.py" ,"put the number here"]**

## Note
*_RSS Feed(http://export.arxiv.org/rss/cs) is not controlled by us there might be somedays when univesrity don't announce new papers and feed will be empty please leave the dataprocessor running it will automatically fetch the result once the data is available in the feed. Python script checks for the length of feed entries if it is > 0 then only it will process the data otherwise skip and print "Nothong to Update"_*

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
