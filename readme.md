## Power grid data analysis pipeline

## Objective
1. Pull data from the National Control Center (NCC) database on a daily basis (@midnight)
2. Store the raw data in an S3 bucket
3. Analyze data from the national SCADA system to identify and clasify events and alarms 
4. Store the cleaned data into an S3 bucket
5. Update the events DB for users
6. Identify critical alarams
7. Create tables and give a sumary status of the national grid (tables in RDS instances)
8. Create a Glue crawl job to catalogue the data and make it available for querrying in Amazon Redshift

## DATA CLEANING
1. Start countdown to keep track of battery banks (applies to station supply fail, battery charger fault,
DC faults etc)
2. Send out emails in case of diff comm failure

## TOOLS
https://excalidraw.com/