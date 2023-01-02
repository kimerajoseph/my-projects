import json
import base64
#import boto3
import os
from datetime import datetime
import awswrangler as wr
import pandas as pd
from sqlalchemy import create_engine

dt = datetime.now().replace(second=0, microsecond=0)

PASSWORD=os.getenv("rds_password")
HOST=os.getenv("rds_host")
DB_NAME=os.getenv("rds_db_name")
DB_USERNAME=os.getenv("rds_username")
S3_BUCKET_NAME=os.getenv("S3_BUCKET")

engine = create_engine(f'mysql+pymysql://{DB_USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}')

#kinesis_client = boto3.client("kinesis")

def clean_data(data):
    data = data[(data.datetime != "time") | (data.event != "event") ]
    #data["event"] = data["event"].str.lower().str.replace(" ","_")
    data["event"] = data["event"].str.lower()

    # covert datetime column to datetime object. SHOULD BE DONE AFTER FILTERING. ELSE, ERRORS
    data.datetime = pd.to_datetime(data.datetime)
    data["date"] = data.datetime.dt.date
    data["month"] = data.datetime.dt.month_name()
    data['weekday'] = data.datetime.dt.day_name()
    data["time"] = data.datetime.dt.time   

    return data

def classify_events(row):
    classify_list = ["trip cct fault","station supply fail","dc power failure","cb lockout locked","cb backup trip",
    "cb back prot trip","dc fault","diff comm fail fault", "cb err status","sf6 lockout", "relay fault"]
    #print(row)  
    for s in classify_list:
        if s in str(row):
            return "critical"

    # mind the indentation. Else, the for loop might check only the first event in the "classify_list"
    else:
        return "normal"  

def get_substation_details():
    sql_qyery = "SELECT * FROM substation_data"
    substation_data = pd.read_sql(sql_qyery,con=engine)
    substation_data.drop(['no','voltage','comments'], axis=1, inplace=True)

    return substation_data

def insert_data_into_db(table_name, df):
    df.to_sql(con=engine, name=table_name, if_exists="append",index=False)

    return

def save_data_to_s3_bucket(my_path, my_df):
    wr.s3.to_parquet(
        df=my_df,
        path=my_path,
        # dataset=True,
        # mode='overwrite'
    )

    return

def rank_voltage_events(row):
    fault_level_rating = {'48v':5,'48':5,'110':5,'110v':5,'station':5,'132':4,'220':4,'400':5,'tx1':3,'tx2':3,
    'tx3':3,'11':2,'33':2,'33kv':2}
    # if key in dict, return value. Else, return 1
    return fault_level_rating.get(row,1)


def lambda_handler(event, context):
    # TODO implement
    df_list = []
    # ITERATE THROUGH EVENTS
    for record in event["Records"]:
        #print(record)
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        decoded_data = eval(decoded_data)
        print(decoded_data)
        #print(decoded_data['data'])
        df_list.append(decoded_data['data'])
    print(len(df_list))

    # create df from events
    df = pd.DataFrame(df_list)


    # call functions to clean data
    if 'datetime' in df.columns: 
        data = clean_data(df)

    # classify cleaned events in the data 
    data['type'] = data['event'].apply(lambda row: classify_events(row))

    # create additional columns
    data["substation_acronym"] = data["event"].apply(lambda x: x.split()[0])
    data["fault_voltage"] = data["event"].apply(lambda x: x.split()[1])

    #print(data)

    # call function to get substation data
    substation_data = get_substation_details()
    #print(substation_data)
    final_data = data.merge(substation_data, how="inner", on="substation_acronym")
    
    # apply fault level code
    final_data['fault_level_code'] = final_data['fault_voltage'].apply(lambda row: rank_voltage_events(row))
    print(final_data.columns)

    final_data["rank"] = final_data[["critical_level","generators","voltage_levels","installed_capacity_(mw)","fault_level_code","region_code"]].apply(tuple,axis=1).rank(method='dense',ascending=False).astype(int)
    # if substations do not belong to UETCL or are not included in the substation list
    if final_data.shape[0] != 0:
        # insert into DB
        insert_data_into_db(table_name="clean_events_data", df=final_data)

        # save to s3 bucket

        save_data_to_s3_bucket(my_path=f"s3://{S3_BUCKET_NAME}/SCADA_PROCESSED_DATA/{dt}_processed_scada_data.parquet", my_df=final_data)

    return 

