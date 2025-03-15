#!/bin/bash

set -e

python -m pip install -r /opt/airflow/requirements/docker_airflowscheduler_req.txt

airflow scheduler &

curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz

./google-cloud-sdk/install.sh --quiet

# Add Google Cloud SDK to PATH immediately (without needing to restart shell)
source /opt/airflow/google-cloud-sdk/path.bash.inc
source /opt/airflow/google-cloud-sdk/completion.bash.inc

gcloud --version

# Authenticate with the service account
gcloud auth activate-service-account adminadmin@dezoomcamp-project2025.iam.gserviceaccount.com --key-file=/opt/airflow/main/keys/sa_adminadmin.json --project=dezoomcamp-project2025

wait
