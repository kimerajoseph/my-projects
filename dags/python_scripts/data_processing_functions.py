import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import os
#from datetime import datetime, timedelta
import awswrangler as wr

host = os.getenv("HOST")
db_username = os.getenv("DB_USERNAME")
password = os.getenv("PASSWORD")
db_name = os.getenv("LOCAL_DB")
port = os.getenv("PORT")

# print(db_username)

engine = create_engine(f'mysql+pymysql://root:{password}@{host}/{db_name}')



###########################################################################
# CLEAN RAW SCADA DATA FUNCTION. 
###########################################################################

def clean_data(data):
    # rename columns
    data = data.drop("index", axis=1)
    data.columns = ['datetime', 'event']
    # filter data 
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

#################################################################################
# CLASSIFY EVENTS
#################################################################################

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


#################################################################################
# GET SUBSTATION DATA DETAILS
#################################################################################
def get_substation_details():
    sql_qyery = "SELECT substation_acronym,critical_level,substation_name FROM substation_data"
    substation_data = pd.read_sql(sql_qyery,con=engine)

    return substation_data


#################################################################################
# INSERT DATA INTO DB
#################################################################################
def insert_data_into_db(table_name, df):
    df.to_sql(con=engine, name=table_name, if_exists="append")

    return

#################################################################################
# WRITE DATA TO S3 BUCKET
#################################################################################
def save_data_to_s3_bucket(my_path, my_df):
    wr.s3.to_parquet(
        df=my_df,
        path=my_path,
        # dataset=True,
        # mode='overwrite'
    )

    return