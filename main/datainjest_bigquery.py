import pyspark
from pyspark.sql import SparkSession
from google.cloud import storage
from datetime import datetime, timedelta

main_dir = "/opt/airflow/main"

spark = SparkSession.builder \
    .appName('stockdata') \
    .getOrCreate()

spark.conf.set('temporaryGcsBucket','dataproc-temp-us-central1-304858319620-9o2qyn2t')

def folders(bucket,prefix):
    client = storage.Client()

    blobs = client.list_blobs(bucket)
    blob_list = [blob.name for blob in blobs]

    blobs = client.list_blobs(bucket, delimiter='/',prefix=prefix)

    folder_list = []

    for page in blobs.pages:
        folder_list.extend(page.prefixes)

    return folder_list

bucket_folders = []
#rawdata/AAPL/
for folder in folders('dezoomcamp_project2025','rawdata/'):
    folder_name = folder#.split('/')[1]
    bucket_folders.append(folder_name)


bigquery_output = 'stocksdata.stock-info'
yesterday = datetime.now().date() - timedelta(days=1)

for folder in bucket_folders:
    bucketfolder = f"gs://dezoomcamp_project2025/{folder}{yesterday}/*/"
    df = spark.read.parquet(bucketfolder)

    df.write.format('bigquery') \
        .option('table',bigquery_output) \
        .mode('append') \
        .save()
