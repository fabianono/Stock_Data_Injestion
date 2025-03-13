#!/bin/bash

set -e

# Install the Python dependencies
python -m pip install -r /opt/airflow/requirements/docker_airflowscheduler_req.txt

# Start the Airflow scheduler
airflow scheduler &

# Download and install the Google Cloud CLI
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz

# Install Google Cloud SDK
./google-cloud-sdk/install.sh --quiet

# Add Google Cloud SDK to PATH immediately (without needing to restart shell)
source /opt/airflow/google-cloud-sdk/path.bash.inc
source /opt/airflow/google-cloud-sdk/completion.bash.inc

# Optionally, you can confirm that gcloud is working:
gcloud --version

# Authenticate with the service account
gcloud auth activate-service-account adminadmin@dezoomcamp-project2025.iam.gserviceaccount.com --key-file=/opt/airflow/main/keys/sa_adminadmin.json --project=dezoomcamp-project2025


# Run the Airflow scheduler in the background (if it's not already running)
# airfow scheduler is already running in the background above, this is just to confirm
# that everything continues as expected.

wait
