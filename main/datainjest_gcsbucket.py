import requests
from dotenv import load_dotenv
import os
import json
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, LongType, TimestampType
from pyspark.sql.functions import col, from_json
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from datetime import datetime, timedelta
import csv

main_dir = "/opt/airflow/main"

credentials_location = f'{main_dir}/keys/sa_adminadmin.json'
jarfile = f"{main_dir}/others/jars/gcs-connector-hadoop3-2.2.5.jar"

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars",jarfile) \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)


sc = SparkContext(conf = conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

spark= SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()


def formatdata(apidata):
    out = []

    yesterday = datetime.now().date() - timedelta(days=1)

    for datetime_key, timeseries_data in apidata["Time Series (30min)"].items():
        formatted_datetime = datetime.strptime(datetime_key, "%Y-%m-%d %H:%M:%S")    
        if formatted_datetime.date() == yesterday:
            data = {
                'StockSymbol': apidata['Meta Data']["2. Symbol"],
                'DateTime': formatted_datetime.isoformat(),
                'Open': float(timeseries_data["1. open"]),
                'High': float(timeseries_data["2. high"]),
                'Low': float(timeseries_data["3. low"]),
                'Close': float(timeseries_data["4. close"]),
                'Volume': int(timeseries_data["5. volume"])
            }
            out.append(data)
        else:
            continue

    return out

stock_schema = StructType([
    StructField("StockSymbol", StringType(), True),
    StructField("DateTime", StringType(), True),
    StructField("Open", FloatType(), True),
    StructField("High", FloatType(), True),
    StructField("Low", FloatType(), True),
    StructField("Close", FloatType(), True),
    StructField("Volume", LongType(), True)
])


with open(f"{main_dir}/others/stocks_symbol.csv", mode = 'r') as file:
    readcsv = csv.reader(file)
    stockslist = [row[0] for row in readcsv]

#keys stored in .env file
load_dotenv()
apikey_evenweekday = os.getenv("stockapikey_evenweekday")
apikey_oddweekday = os.getenv("stockapikey_oddweekday") 

gcs_bucket = "gs://dezoomcamp_project2025/rawdata/"

date_saved = datetime.now().date() - timedelta(days=1)

print(f"Day id: {date_saved.weekday()}")

#Rotating between 2 API keys due to limit calls since the accounts are from the free tier
if (date_saved.weekday())%2 == 0:
    apikey = apikey_evenweekday
else:
    apikey = apikey_oddweekday

#No data to run since stock market closed
if date_saved.weekday() in [5,6]:
    print("Yesterday was the weekend. Stock market was not open.")
else:
    for stock in stockslist:
        stockapi = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=30min&apikey={apikey}"
        resp = requests.get(url=stockapi)
        data = formatdata(resp.json())
        print(json.dumps(data, indent = 4))
        df_stock = spark.createDataFrame(data, stock_schema)
        df_stock = df_stock.withColumn("DateTime", col("DateTime").cast("timestamp"))
        
        location = f"{gcs_bucket}/{stock}/{date_saved}"
        print("Writing to bucket")
        df_stock.coalesce(1).write.parquet(location, mode='overwrite')
    
    print("injestion ended")

