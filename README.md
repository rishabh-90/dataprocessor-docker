# dataprocessor-docker
Simple Data Processor built using Docker

Dataprocessor is checking for new feed after **Nth Minute** which can be changed in the **Dockerfile of part1 cmd section** after filename third arugment is minutes for eg: **CMD [ "python", "dataProcessor.py" ,"put the number here"]**

## Note
*_RSS Feed(http://export.arxiv.org/rss/cs) is not controlled by us. There might be somedays when univesrity don't announce new papers and feed will be empty. Please leave the dataprocessor running. It will automatically fetch the result once the data is available in the feed. Python script checks for the length of feed entries - if len(feed.enteries)> 0 only then it will process the data otherwise skip and print "Nothing to Update"_*

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
