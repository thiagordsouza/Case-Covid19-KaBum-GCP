import pandas as pd
from pandas.io import gbq
from google.cloud import bigquery

# Libs
# gcsfs
# fsspec
# pandas
# pandas-gbq

def hello_gcs(event, context):
    lst = []
    file_name = event['name']
    table_name = file_name.split('.')[0]

    # Event,File metadata details writing into Big Query
    dct = {
     'Event_ID':context.event_id,
     'Event_type':context.event_type,
     'Bucket_name':event['bucket'],
     'File_name':event['name'],
     'Created':event['timeCreated'],
     'Updated':event['updated']
     }
    lst.append(dct)
    df_metadata = pd.DataFrame.from_records(lst)
    df_metadata.to_gbq('covid2.data_loading_metadata', 
                        project_id='casecovidkabum', 
                        if_exists='append',
                        location='southamerica-east1')
    
    # Actual file data , writing to Big Query
    df_data = pd.read_csv('gs://' + event['bucket'] + '/' + file_name, encoding='UTF-8')
    df_data['date'] = pd.to_datetime(df_data['date'])

    df_data.to_gbq('covid2.' + table_name, 
                        project_id='casecovidkabum', 
                        if_exists='replace',
                        location='southamerica-east1')