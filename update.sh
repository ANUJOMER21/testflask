#!/bin/bash

# Navigate to project directory
cd /path/to/your-repo

# Pull latest changes from GitHub
git pull origin main

# Rebuild Docker image
docker-compose build --no-cache

# Redeploy with zero downtime
docker-compose up -d --no-deps --build flask-app