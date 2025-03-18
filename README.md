# Stock Data Injestion DEMO
### Basic stock data injestion for the top 10 stocks in the US stock market by market cap

**Just a note that this current project is running as a free tiered subscription to Google Cloud. Access will end on June 2 2025, so if the code is still working, it will stop working when the free tier access end.**

In this demo project:
1. Data is obtained via a GET request from the TIME_SERIES_INTRADAY api which can be found [here](https://www.alphavantage.co/documentation/). Data is obtained via batch request.
2. The script is scheduled by *airflow*(a scheduler that runs tasks) to run a few hours after the stock market closes. This allows the API some time for the data to be loaded. Will injest the data at 30 mins interval.  
3. Data in transformed and then uploaded to a GCS bucket via spark.
4. The next script then runs through *airflow* which uploads the day's data from the GCS bucket to BigQuery using Google's dataproc spark.
5. Looker studio is used to extract data and provide some data visualization.


### Process mapping:
![alt text](StockData-ProcessMap.jpg)

- Terraform used to create a linux VM instance, GCS bucket and Dataproc clusters.
- Sandboxing via a VM, docker compose, python venv.


### Data Visualization:
Dashboard can be found [here](https://lookerstudio.google.com/reporting/ce71aea8-07a7-4c67-8051-f9412e5136f5)
![alt text](Stock_Market_Report.jpg)

- Provides a snap shot of how the top 10 stocks in the US market (provided in the csv [here](https://github.com/fabianono/Stock_Data_Injestion/blob/master/others/stocks_symbol.csv)) impacts the S&P500 (SPY) in a selected time period.
- Also shows the traded volume of the top 10 US stocks in the selected time period.