#!/bin/bash

# Script to load seed data into the database

echo "Loading seed data into database..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

# Load seed data
docker compose exec -T db psql -U interview_user -d interview_ai < seeds/seed.sql

echo "Seed data loaded successfully!"
echo "Demo data includes:"
echo "- 3 candidates"
echo "- 1 vacancy (Backend Developer)"
echo "- 8 questions with criteria"
echo "- 1 completed interview session"
