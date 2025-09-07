#!/bin/bash

# Deploy script for Interview AI system
set -e

echo "🚀 Starting deployment..."

# Configuration
PROJECT_DIR="/opt/more.tech.2025"
BACKUP_DIR="/backup/$(date +%Y%m%d_%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found. Are you in the project directory?"
    exit 1
fi

# Create backup directory
print_status "Creating backup..."
mkdir -p "$BACKUP_DIR"

# Backup current configuration
if [ -f "Caddyfile" ]; then
    cp Caddyfile "$BACKUP_DIR/"
    print_status "Caddyfile backed up to $BACKUP_DIR"
fi

# Pull latest changes
print_status "Pulling latest changes from git..."
git pull origin main

# Stop containers gracefully
print_status "Stopping containers..."
docker-compose down

# Remove old images to free space
print_status "Cleaning up old Docker images..."
docker system prune -f

# Build new images
print_status "Building new images..."
docker-compose build --no-cache

# Start containers
print_status "Starting containers..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 30

# Health check
print_status "Performing health check..."
if curl -f -k https://localhost > /dev/null 2>&1; then
    print_status "✅ Health check passed!"
else
    print_error "❌ Health check failed!"
    print_status "Checking container status..."
    docker-compose ps
    exit 1
fi

# Show container status
print_status "Container status:"
docker-compose ps

# Show logs for any failed containers
print_status "Checking for failed containers..."
FAILED_CONTAINERS=$(docker-compose ps --services --filter "status=exited")
if [ ! -z "$FAILED_CONTAINERS" ]; then
    print_warning "Some containers failed to start:"
    for container in $FAILED_CONTAINERS; do
        print_error "Container $container failed. Logs:"
        docker-compose logs "$container" --tail=20
    done
    exit 1
fi

print_status "🎉 Deployment completed successfully!"
print_status "Site should be available at: https://moretech2025clvb.ru"
