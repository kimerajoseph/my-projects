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

## STRUCTURE
1. All data processing functions are put in the "data_processing_functions.py" file. this ensures that they
are written once and called from any python script
2. Functions are not included in DAGs. They are simply called. This is meant to keep the DAGs simple
3. We use xcom to pass data between DAGs. We only pass parameters (no big data files passed). xcom clears
the DAG xcom parameters for each run

## RANK CRITICAL EVENTS
1. Much as some events are all critical, we have to rank already critical events in order of importance
Rating is based on critical level, substation location, installed capacity, generation presence etc
2. Events are ranked and teams dispatched based on their ranks
3. create bins for installed capacity. Because the values are high, when sorting, this values has much
greater influence than the rest. The rest are categorical
3. Some events need timers eg battery bank faults to track time before batteries are drained and disaster 
potentially strikes
## TOOLS
https://excalidraw.com/