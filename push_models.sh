#!/bin/bash

# Define local and remote paths
LOCAL_DIR="pca_models/"
REMOTE_USER="root"
REMOTE_HOST="192.168.1.13"
REMOTE_DIR="/home/frataga/Frataga/"

# Copy files recursively using scp
scp -r "$LOCAL_DIR" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"
