import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta
import awswrangler as wr
import logging

# get environmental variables
host = os.getenv("HOST")
db_username = os.getenv("DB_USERNAME")
password = os.getenv("PASSWORD")
db_name = os.getenv("LOCAL_DB")
port = os.getenv("PORT")
s3_bucket = os.getenv("BUCKET_NAME")
project_folder = os.getenv("GRID_FOLDER")

# CREATE ENGINE
engine = create_engine(f'mysql+pymysql://root:{password}@{host}/{db_name}')

# IMPORT REQUIRED DATA CLEANINING FUNCTIONS
from python_scripts import data_processing_functions

def get_raw_data_from_scada_table(past_days):
    sql_query = "SELECT * FROM scada_data WHERE DATE(datetime) = %(serach_date)s"
    my_search_date = datetime.strftime(datetime.now() - timedelta(past_days), '%Y-%m-%d')
    my_params={"serach_date":my_search_date}
    filtered_data = pd.read_sql(sql_query,con=engine, params=my_params)
    #print("filtered data", filtered_data.shape)

    # name file using dates
    file_name = f"{my_search_date}_scada_data.parquet"
    #print("FILENAME: ",file_name)
    #try:
    s3_file_path=f's3://{s3_bucket}/{project_folder}/{file_name}'
    #print("s3_file_path: ",s3_file_path)
    wr.s3.to_parquet(
        df=filtered_data,
        path=s3_file_path,
        # dataset=True,
        # mode='overwrite',
    )
    #print("file path", s3_file_path)
    return s3_file_path

    # except Exception as err:
    #     logging.error(err)

def process_raw_data(task_filename):
    # call data cleaning function
    data = wr.s3.read_parquet(task_filename)
    data = data_processing_functions.clean_data(data)

    # call data classifying function
    data['type'] = data['event'].apply(lambda row: data_processing_functions.classify_events(row))

    # create columns
    data["substation_acronym"] = data["event"].apply(lambda x: x.split()[0])
    data["fault_voltage"] = data["event"].apply(lambda x: x.split()[1])

    # call function to get substation data
    substation_data = data_processing_functions.get_substation_details()
    final_data = data.merge(substation_data, how="inner", on="substation_acronym")

    return final_data



