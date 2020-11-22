# README
___
* LAST UPDATED: 2020-10-26
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: ay2021-1
* FOLDER: project/brain-bot

## Files
* [brainbot-processing-script.py](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/brain-bot/brainbot_processing_script.py)
* [brainbot-process-doc.txt](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/brain-bot/brainbot-process-doc.txt)

### brainbot-processing-script.py
___
#### How It Works

brainbot-processing-script.py creates a new CSV file called 'Sea_Duck_Migration.csv'. Once this is done, it reads an existing CSV file called 'Migration Patterns of Pacific Sea Ducks.csv', and stores the timestamp, location-long, location-lat, and tag-local-identifier variables for data that was collected in May 2014. 

#### Necessary Packages
* [csv](https://www.howtogeek.com/348960/what-is-a-csv-file-and-how-do-i-open-it/)

#### Input files
* [Migration Patterns of Pacific Sea Ducks.csv](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/brain-bot/Migration%20Patterns%20of%20Pacific%20Sea%20Ducks.csv)

#### Output files
* [Sea_Duck_Migration.csv](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/brain-bot/Sea_Duck_Migration.csv)

### Pacific Sea Duck Migration Data
* Source: [Movebank](https://www.movebank.org/cms/webapp?gwt_fragment=page=studies,path=study6506971)

* Variables Used:
  + timestamp: Date and time that data was recorded
  + location-long: Longitude location of duck
  + location-lat: Latitude location of duck
  + tag-local-identifier: unique tag number of duck
  

* Contact person: Sean Boyd (sean.boyd@ec.gc.ca)
* Institution: Max Planck Institue of Animal Behavior

