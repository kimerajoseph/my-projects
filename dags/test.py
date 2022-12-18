from python_scripts import scada_data_processing, data_processing_functions
import pandas as pd

def get_scada_data():

    # call function
    target_filename = scada_data_processing.get_raw_data_from_scada_table(past_days=37)
    # ti.xcom_push(key='s3_filename', value=target_filename)
    return target_filename

def process_and_analyze_scada_data():
    #task_filename=ti.xcom_pull(key='s3_filename', task_ids='extract_target_data')
    task_filename = get_scada_data()
    cleaned_data = scada_data_processing.process_raw_data(task_filename)
    print(cleaned_data.shape)

    # insert data into db
    data_processing_functions.insert_data_into_db(table_name="final_processed_data", df=cleaned_data)

    # save data into s3 bucket
    data_processing_functions.save_data_to_s3_bucket(
        my_path="s3://my-projects-jkimera/grid-project/processed_scada_data.parquet",
        my_df=cleaned_data
    )
    

    

process_and_analyze_scada_data()