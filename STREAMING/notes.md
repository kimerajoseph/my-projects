## BINARY LOG
The binary log contains “events” that describe database changes such as table creation operations or changes to table data. It also contains events for statements that potentially could have made changes (for example, a DELETE which matched no rows). The binary log also contains information about how long each statement took that updated data. The binary log has two important purposes:

For replication, the binary log on a replication source server provides a record of the data changes to be sent to replicas. The source sends the events contained in its binary log to its replicas, which execute those events to make the same data changes that were made on the source.

Certain data recovery operations require use of the binary log. After a backup has been restored, the events in the binary log that were recorded after the backup was made are re-executed. 

The binary log is not used for statements such as SELECT or SHOW that do not modify data.

### Following are the types of the binary logging:

Statement-based: The events in this binary log contain the DML queries (Insert, Update, and Delete) used to change the data
Row-based: The events in this binary log describe changes that occurred on the individual rows of the tables
Mixed-Logging: In the mixed-logging mode, by default, MySQL uses statement-based logging, but if required, it automatically changes to row-based logging

## CHECK IF LOGGING IS ENABLED
1. open mysql commandline. type "show global variables like ‘log_bin’;"
2. confirm if log_bin is enabled
3. if off, go to C:\ProgramData\MySQL\MySQL Server 8.0, open my.ini file and set log-bin=”[PC-NAME]-bin”
4. open windows powershell and run "Restart-Service MySQL80"
5. To disable the binary logging, add the following lines in the my.ini file.
[mysqld]
skip-log-bin
6. Restart the MySQL services.
7. SET bin log format: mysql> SET GLOBAL binlog_format = 'ROW';
7. To view the default location of the binary location, execute the following query;
mysql> show global variables like '%log_bin%';
8. To view the list of the binary logs, run the below command in MySQL command line utility:
mysql> show binary logs;

TO RESTART mysql, press windows button >> services >> mysql

## CREATE REPLICA ON MYSQL DB
1. create a user
mysql> CREATE USER 'repl'@'%.example.com' IDENTIFIED BY 'password';
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%.example.com';

2. create data dump
C:\Program Files\MySQL\MySQL Server 8.0\bin\
- RUN CMD
mysqldump.exe –u root -p [db_name] -h [hostname] > C:\[filename].sql
Enter DB password


