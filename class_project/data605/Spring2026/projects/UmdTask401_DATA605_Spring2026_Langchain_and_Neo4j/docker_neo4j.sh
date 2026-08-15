#!/bin/bash
# """
# Start the Neo4j Docker container for the LangChain + Neo4j project.
#
# This script is idempotent:
#   - If the neo4j container is already running, it does nothing.
#   - If the container exists but is stopped, it restarts it.
#   - If the container does not exist, it creates and starts it.
#
# Neo4j will be accessible at:
#   - Browser UI: http://localhost:7474
#   - Bolt (driver): bolt://localhost:7687
#
# Usage:
#   > ./docker_neo4j.sh
# """

# Exit immediately if any command exits with a non-zero status.
set -e

NEO4J_IMAGE="neo4j:5.26.24"
NEO4J_CONTAINER="neo4j"
NEO4J_PASSWORD="password"

echo "Checking Neo4j container status..."

# Check if container is already running.
if docker ps --format '{{.Names}}' | grep -q "^${NEO4J_CONTAINER}$"; then
    echo "Neo4j is already running."
    echo "  Browser UI : http://localhost:7474"
    echo "  Bolt URI   : bolt://localhost:7687"
    exit 0
fi

# Check if container exists but is stopped.
if docker ps -a --format '{{.Names}}' | grep -q "^${NEO4J_CONTAINER}$"; then
    echo "Restarting existing Neo4j container..."
    docker start $NEO4J_CONTAINER
else
    echo "Creating and starting Neo4j container ($NEO4J_IMAGE)..."
    docker run -d \
        --name $NEO4J_CONTAINER \
        -p 7474:7474 \
        -p 7687:7687 \
        -e NEO4J_AUTH=neo4j/$NEO4J_PASSWORD \
        $NEO4J_IMAGE
fi

echo ""
echo "Neo4j is starting — wait ~20 seconds before connecting."
echo "  Browser UI : http://localhost:7474"
echo "  Bolt URI   : bolt://localhost:7687"
echo "  Username   : neo4j"
echo "  Password   : $NEO4J_PASSWORD"
