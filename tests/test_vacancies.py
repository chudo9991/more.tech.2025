"""
Tests for vacancy API
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_vacancy():
    """Test creating a vacancy"""
    vacancy_data = {
        "title": "Business Analyst",
        "status": "active",
        "region": "Москва",
        "city": "Москва",
        "employment_type": "full",
        "salary_min": 100000,
        "salary_max": 150000,
        "requirements": "Опыт работы от 2 лет",
        "responsibilities": "Анализ бизнес-процессов"
    }
    
    response = client.post("/api/v1/vacancies/", json=vacancy_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Business Analyst"
    assert data["vacancy_code"].startswith("BA-")
    assert data["status"] == "active"
    assert data["region"] == "Москва"


def test_get_vacancies():
    """Test getting vacancies list"""
    response = client.get("/api/v1/vacancies/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_get_vacancy_statistics():
    """Test getting vacancy statistics"""
    response = client.get("/api/v1/vacancies/statistics")
    assert response.status_code == 200
    
    data = response.json()
    assert "total" in data
    assert "active" in data
    assert "closed" in data
    assert "draft" in data


def test_search_vacancies():
    """Test searching vacancies"""
    response = client.get("/api/v1/vacancies/search?q=Business")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
