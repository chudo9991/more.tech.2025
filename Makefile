.PHONY: help up down build logs clean test lint seed demo health test-sip test-interview demo-full

# Default target
help:
	@echo "Available commands:"
	@echo "  up      - Start all services"
	@echo "  down    - Stop all services"
	@echo "  build   - Build all Docker images"
	@echo "  logs    - Show logs from all services"
	@echo "  clean   - Remove containers, volumes, and images"
	@echo "  test    - Run tests for all services"
	@echo "  lint    - Run linters for all services"
	@echo "  seed    - Load seed data into database"
	@echo "  demo    - Run demo script"
	@echo "  health  - Check health of all services"
	@echo "  test-sip - Test SIP simulator (call flow)"
	@echo "  test-interview - Test full interview simulation"
	@echo "  demo-full - Run complete system demo"

# Start all services
up:
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@make health

# Stop all services
down:
	@echo "Stopping all services..."
	docker-compose down

# Build all Docker images
build:
	@echo "Building all Docker images..."
	docker-compose build --no-cache

# Show logs from all services
logs:
	docker-compose logs -f

# Clean up everything
clean:
	@echo "Cleaning up containers, volumes, and images..."
	docker-compose down -v --rmi all
	docker system prune -f

# Run tests for all services
test:
	@echo "Running tests for orchestrator..."
	cd orchestrator && make test
	@echo "Running tests for stt..."
	cd stt && make test
	@echo "Running tests for tts..."
	cd tts && make test
	@echo "Running tests for scoring..."
	cd scoring && make test
	@echo "Running tests for frontend..."
	cd frontend && make test

# Run linters for all services
lint:
	@echo "Running linters for orchestrator..."
	cd orchestrator && make lint
	@echo "Running linters for stt..."
	cd stt && make lint
	@echo "Running linters for tts..."
	cd tts && make lint
	@echo "Running linters for scoring..."
	cd scoring && make lint
	@echo "Running linters for frontend..."
	cd frontend && make lint

# Load seed data
seed:
	@echo "Loading seed data..."
	@if [ -f "scripts/seed.sh" ]; then \
		./scripts/seed.sh; \
	else \
		docker-compose exec db psql -U interview_user -d interview_ai -f /docker-entrypoint-initdb.d/seed.sql; \
	fi

# Run demo script
demo:
	@echo "Running demo script..."
	@if [ -f "scripts/demo.sh" ]; then \
		chmod +x scripts/demo.sh && ./scripts/demo.sh; \
	else \
		echo "Demo script not found. Creating basic demo..."; \
		curl -f http://localhost:8000/healthz && echo "Orchestrator: OK"; \
		curl -f http://localhost:8001/healthz && echo "STT: OK"; \
		curl -f http://localhost:8002/healthz && echo "TTS: OK"; \
		curl -f http://localhost:8003/healthz && echo "Scoring: OK"; \
		curl -f http://localhost:3000 && echo "Frontend: OK"; \
	fi

# Check health of all services
health:
	@echo "Checking service health..."
	@echo "Database:"
	@curl -s http://localhost:5432 > /dev/null && echo "  ✓ PostgreSQL" || echo "  ✗ PostgreSQL"
	@echo "MinIO:"
	@curl -s http://localhost:9000/minio/health/live > /dev/null && echo "  ✓ MinIO" || echo "  ✗ MinIO"
	@echo "Orchestrator:"
	@curl -s http://localhost:8000/healthz > /dev/null && echo "  ✓ Orchestrator" || echo "  ✗ Orchestrator"
	@echo "STT Service:"
	@curl -s http://localhost:8001/healthz > /dev/null && echo "  ✓ STT" || echo "  ✗ STT"
	@echo "TTS Service:"
	@curl -s http://localhost:8002/healthz > /dev/null && echo "  ✓ TTS" || echo "  ✗ TTS"
	@echo "Scoring Service:"
	@curl -s http://localhost:8003/healthz > /dev/null && echo "  ✓ Scoring" || echo "  ✗ Scoring"
	@echo "Frontend:"
	@curl -s http://localhost:3000 > /dev/null && echo "  ✓ Frontend" || echo "  ✗ Frontend"

# Development helpers
dev-up:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dev-down:
	@echo "Stopping development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

# Database helpers
db-migrate:
	@echo "Running database migrations..."
	docker-compose exec orchestrator alembic upgrade head

db-rollback:
	@echo "Rolling back last migration..."
	docker-compose exec orchestrator alembic downgrade -1

db-reset:
	@echo "Resetting database..."
	docker-compose down -v
	docker-compose up -d db
	@sleep 10
	@make db-migrate
	@make seed

db-init:
	@echo "Initializing database with migrations..."
	docker-compose exec orchestrator alembic upgrade head

db-status:
	@echo "Checking migration status..."
	docker-compose exec orchestrator alembic current

db-history:
	@echo "Migration history..."
	docker-compose exec orchestrator alembic history

# Logs for specific services
logs-orchestrator:
	docker-compose logs -f orchestrator

logs-stt:
	docker-compose logs -f stt

logs-tts:
	docker-compose logs -f tts

logs-scoring:
	docker-compose logs -f scoring

logs-frontend:
	docker-compose logs -f frontend

# Shell access to services
shell-orchestrator:
	docker-compose exec orchestrator /bin/bash

shell-db:
	docker-compose exec db psql -U interview_user -d interview_ai

shell-minio:
	docker-compose exec minio /bin/sh

# Testing commands
test-sip:
	@echo "Testing SIP simulator..."
	@python scripts/sip_simulator.py http://localhost:8000 call

test-interview:
	@echo "Testing full interview simulation..."
	@python scripts/sip_simulator.py http://localhost:8000 interview

demo-full:
	@echo "Running complete system demo..."
	@python scripts/demo.py http://localhost:8000
