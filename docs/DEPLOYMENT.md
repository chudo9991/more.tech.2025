# Варианты деплоя

## 1. Локальный деплой (текущий)

Используется в CI/CD pipeline. Деплой происходит на том же сервере, где запускается GitHub Actions.

### Преимущества:
- Не требует дополнительной инфраструктуры
- Простота настройки
- Подходит для демо и тестирования

### Недостатки:
- Ограниченные ресурсы GitHub Actions
- Нет постоянного доступа к приложению
- Не подходит для production

### Настройка:
```yaml
# В .github/workflows/ci-cd.yml
- name: Deploy to staging
  run: |
    echo "Deploying to staging environment..."
    
    # Создаем staging окружение
    mkdir -p staging
    cp docker-compose.prod.yml staging/
    cp env.prod.sample staging/.env.prod
    
    # Обновляем теги образов
    sed -i "s|image: .*/orchestrator:.*|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/orchestrator:${{ steps.meta.outputs.version }}|g" staging/docker-compose.prod.yml
    # ... остальные сервисы
    
    # Запускаем staging
    cd staging
    docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## 2. Деплой на VPS сервер

Арендуете VPS (DigitalOcean, AWS EC2, Hetzner) и деплоите туда.

### Преимущества:
- Полный контроль над инфраструктурой
- Постоянный доступ к приложению
- Подходит для production
- Низкая стоимость

### Недостатки:
- Требует настройки сервера
- Нужно управлять обновлениями и безопасностью

### Настройка:

#### 2.1. Подготовка сервера
```bash
# Установка Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2.2. Настройка CI/CD
```yaml
# В .github/workflows/ci-cd.yml
- name: Deploy to VPS
  run: |
    echo "Deploying to VPS server..."
    
    # Копируем файлы на сервер
    scp docker-compose.prod.yml ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }}:/opt/interview-ai/
    scp env.prod.sample ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }}:/opt/interview-ai/.env.prod
    
    # Деплоим на сервер
    ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'EOF'
      cd /opt/interview-ai
      
      # Обновляем образы
      docker compose -f docker-compose.prod.yml pull
      
      # Перезапускаем сервисы
      docker compose -f docker-compose.prod.yml down
      docker compose -f docker-compose.prod.yml up -d
      
      # Проверяем статус
      docker compose -f docker-compose.prod.yml ps
    EOF
```

#### 2.3. GitHub Secrets для VPS
```
SERVER_HOST=your-server-ip
SERVER_USER=your-username
SERVER_SSH_KEY=your-private-ssh-key
```

## 3. Деплой в Kubernetes

Используете Kubernetes кластер (GKE, EKS, AKS).

### Преимущества:
- Высокая доступность
- Автоматическое масштабирование
- Продвинутое управление ресурсами
- Подходит для enterprise

### Недостатки:
- Сложность настройки
- Высокая стоимость
- Требует знаний Kubernetes

### Настройка:

#### 3.1. Kubernetes манифесты
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestrator
spec:
  replicas: 2
  selector:
    matchLabels:
      app: orchestrator
  template:
    metadata:
      labels:
        app: orchestrator
    spec:
      containers:
      - name: orchestrator
        image: ghcr.io/your-username/more.tech.2025/orchestrator:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
```

#### 3.2. CI/CD для Kubernetes
```yaml
# В .github/workflows/ci-cd.yml
- name: Deploy to Kubernetes
  run: |
    echo "Deploying to Kubernetes..."
    
    # Обновляем образы в деплойментах
    kubectl set image deployment/orchestrator orchestrator=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/orchestrator:${{ steps.meta.outputs.version }}
    kubectl set image deployment/stt stt=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/stt:${{ steps.meta.outputs.version }}
    kubectl set image deployment/llm llm=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/llm:${{ steps.meta.outputs.version }}
    kubectl set image deployment/avatar avatar=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/avatar:${{ steps.meta.outputs.version }}
    kubectl set image deployment/scoring scoring=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/scoring:${{ steps.meta.outputs.version }}
    kubectl set image deployment/frontend frontend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/frontend:${{ steps.meta.outputs.version }}
    
    # Ждем обновления
    kubectl rollout status deployment/orchestrator
    kubectl rollout status deployment/stt
    kubectl rollout status deployment/llm
    kubectl rollout status deployment/avatar
    kubectl rollout status deployment/scoring
    kubectl rollout status deployment/frontend
```

## 4. Деплой в облачные платформы

### 4.1. Google Cloud Run
```yaml
- name: Deploy to Cloud Run
  run: |
    echo "Deploying to Google Cloud Run..."
    
    # Деплой каждого сервиса
    gcloud run deploy orchestrator \
      --image ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/orchestrator:${{ steps.meta.outputs.version }} \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
```

### 4.2. AWS ECS
```yaml
- name: Deploy to ECS
  run: |
    echo "Deploying to AWS ECS..."
    
    # Обновляем task definition
    aws ecs register-task-definition --cli-input-json file://task-definition.json
    
    # Обновляем сервис
    aws ecs update-service --cluster interview-ai --service orchestrator --task-definition orchestrator
```

## Рекомендации по выбору

### Для MVP/Демо:
- **Локальный деплой** (вариант 1)

### Для Production с ограниченным бюджетом:
- **VPS сервер** (вариант 2)

### Для Enterprise/Масштабируемых проектов:
- **Kubernetes** (вариант 3)

### Для быстрого старта в облаке:
- **Cloud Run/ECS** (вариант 4)

## Мониторинг и логирование

### Логи
```bash
# Docker Compose
docker compose -f docker-compose.prod.yml logs -f

# Kubernetes
kubectl logs -f deployment/orchestrator

# Cloud Run
gcloud logging read "resource.type=cloud_run_revision"
```

### Мониторинг
```bash
# Health checks
curl http://your-domain/healthz

# Метрики
docker stats
kubectl top pods
```

## Безопасность

### Переменные окружения
- Все секреты храните в GitHub Secrets
- Используйте внешние secret managers (AWS Secrets Manager, GCP Secret Manager)
- Не коммитьте .env файлы

### Сеть
- Используйте HTTPS
- Настройте firewall
- Ограничьте доступ к портам

### Обновления
- Регулярно обновляйте базовые образы
- Сканируйте образы на уязвимости
- Используйте multi-stage builds
