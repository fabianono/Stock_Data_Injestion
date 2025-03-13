#!/bin/bash

spark_sql_kafka="https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.5/spark-sql-kafka-0-10_2.12-3.5.5.jar"
kafka_clients="https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.9.0/kafka-clients-3.9.0.jar"
spark_token_provider_kafka="https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.5/spark-token-provider-kafka-0-10_2.12-3.5.5.jar"
common_pools2="https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.1/commons-pool2-2.12.1.jar"


gcs_bucket="gs://dezoomcamp_project2025/jars"

curl -s "$spark_sql_kafka" | gsutil cp - "$gcs_bucket/spark_sql_kafka.jar"
curl -s "$kafka_clients" | gsutil cp - "$gcs_bucket/kafka_clients.jar" 
curl -s "$spark_token_provider_kafka" | gsutil cp - "$gcs_bucket/spark_token_provider_kafka.jar" 
curl -s "$common_pools2" | gsutil cp - "$gcs_bucket/common_pools2.jar" 

