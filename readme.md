## PROJECT
Real-time data streaming pipelines to draw insights from power system data

## OBJECTIVES
1. Aid power system operators in identifying and hihlighting critical events and alarms
2. Enable technical teams identify and respond to power system faults
3. Send notifications to teams alerting them on ciritical events
4. Analyze and process events data for further analysis

## SET UP
1. Events streamed into on-premise SCADA system from IoTs in the field
2. Replication is setup betwwen the SCADA system and a cloud AWS RDS MYSQL instance (changes in on-premise DB are replicated in the cloud)
3. The RDS DB is converted into a stream with the help of AWS DMS
4. All changes in the RDS DB are streamed to a Kinesis stream 
5. The Kinesis stream  delivers the raw data to an s3 bucket
6. The Kinesis stream also invokes a Lambda every 1 min (or after 5 MB buffer) that processes the data. Lambda adds context, processes the data and ranks events
7. Lambda inserts the processed data into another DB for end users to use (end users include system controllers, energy sales, compliance etc)
