#!/bin/bash


# Fetch latest changes from GitHub
git fetch origin

# Check if there are new changes in the main branch
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "New changes detected, pulling updates..."
    git pull origin main

    # Rebuild Docker image
    docker compose build --no-cache

    # Redeploy with zero downtime
    docker compose up -d --no-deps --build flask-app

    echo "Update completed at $(date)"
else
    echo "No changes detected at $(date)"
fi