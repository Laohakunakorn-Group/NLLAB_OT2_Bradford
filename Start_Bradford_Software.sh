#!/bin/bash

# Navigate to the directory where the script file is located
cd "$(dirname "$0")"

# Start Docker Compose
docker-compose up -d

# Wait for a few seconds to ensure Docker services are up
sleep 10

# Open a URL in the default browser
open http://localhost:8052/
