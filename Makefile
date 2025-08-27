# Makefile for Interview AI Project

.PHONY: help build test deploy clean logs health

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build all Docker images"
	@echo "  test      - Run tests"
	@echo "  up        - Start development environment"
	@echo "  up-prod   - Start production environment"
	@echo "  down      - Stop all services"
	@echo "  logs      - Show logs for all services"
	@echo "  health    - Check health of all services"
	@echo "  clean     - Clean up containers and images"
	@echo "  deploy    - Deploy to production"

# Development environment
up:
	docker compose up -d
	@echo "Development environment started!"
	@echo "Frontend: http://localhost:3000"
	@echo "HR Panel: http://localhost:3000/hr"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "MinIO Console: http://localhost:9001"

# Production environment
up-prod:
	@if [ ! -f .env.prod ]; then \
		echo "Error: .env.prod file not found!"; \
		echo "Please copy env.prod.sample to .env.prod and configure it."; \
		exit 1; \
	fi
	docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
	@echo "Production environment started!"

# Stop all services
down:
	docker compose down
	docker compose -f docker-compose.prod.yml down 2>/dev/null || true

# Build all images
build:
	docker compose build
	@echo "All images built successfully!"

# Run tests
test:
	docker compose -f docker-compose.test.yml up --abort-on-container-exit
	@echo "Tests completed!"

# Show logs
logs:
	docker compose logs -f

# Check health
health:
	@echo "Checking service health..."
	@curl -f http://localhost:8000/healthz && echo "✓ Orchestrator" || echo "✗ Orchestrator"
	@curl -f http://localhost:8001/healthz && echo "✓ STT" || echo "✗ STT"
	@curl -f http://localhost:8004/healthz && echo "✓ LLM" || echo "✗ LLM"
	@curl -f http://localhost:8005/healthz && echo "✓ Avatar" || echo "✗ Avatar"
	@curl -f http://localhost:8003/healthz && echo "✓ Scoring" || echo "✗ Scoring"
	@curl -f http://localhost:3000 && echo "✓ Frontend" || echo "✗ Frontend"

# Clean up
clean:
	docker compose down -v --remove-orphans
	docker compose -f docker-compose.prod.yml down -v --remove-orphans 2>/dev/null || true
	docker system prune -f
	@echo "Cleanup completed!"

# Database operations
db-shell:
	docker compose exec db psql -U postgres -d interview_ai

db-reset:
	docker compose down -v
	docker compose up -d db
	@echo "Database reset completed!"

# MinIO operations
minio-shell:
	docker compose exec minio mc

minio-init:
	docker compose exec minio mc mb minio/audio-files --ignore-existing
	@echo "MinIO buckets initialized!"

# Development helpers
dev-logs:
	docker compose logs -f orchestrator stt llm avatar scoring

frontend-logs:
	docker compose logs -f frontend

# Production deployment
deploy:
	@if [ ! -f .env.prod ]; then \
		echo "Error: .env.prod file not found!"; \
		echo "Please copy env.prod.sample to .env.prod and configure it."; \
		exit 1; \
	fi
	@echo "Deploying to production..."
	docker compose -f docker-compose.prod.yml --env-file .env.prod pull
	docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
	@echo "Production deployment completed!"

# CI/CD helpers
ci-build:
	docker compose build --no-cache
	@echo "CI build completed!"

ci-test:
	docker compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test
	@echo "CI tests completed!"

# Monitoring
status:
	@echo "Service Status:"
	@docker compose ps

# Backup and restore
backup:
	@echo "Creating backup..."
	docker compose exec db pg_dump -U postgres interview_ai > backup_$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup created!"

restore:
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Error: Please specify BACKUP_FILE=filename.sql"; \
		exit 1; \
	fi
	@echo "Restoring from $(BACKUP_FILE)..."
	docker compose exec -T db psql -U postgres interview_ai < $(BACKUP_FILE)
	@echo "Restore completed!"
