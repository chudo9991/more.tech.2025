import pytest
import httpx
import asyncio
from typing import List

# Test configuration
SERVICES = [
    {"name": "orchestrator", "port": 8000},
    {"name": "stt", "port": 8001},
    {"name": "llm", "port": 8004},
    {"name": "avatar", "port": 8005},
    {"name": "scoring", "port": 8003},
]

@pytest.mark.asyncio
async def test_orchestrator_health():
    """Test orchestrator health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://orchestrator:8000/healthz")
        assert response.status_code == 200
        assert response.text.strip() == "healthy"

@pytest.mark.asyncio
async def test_stt_health():
    """Test STT service health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://stt:8001/healthz")
        assert response.status_code == 200
        assert response.text.strip() == "healthy"

@pytest.mark.asyncio
async def test_llm_health():
    """Test LLM service health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://llm:8004/healthz")
        assert response.status_code == 200
        assert response.text.strip() == "healthy"

@pytest.mark.asyncio
async def test_avatar_health():
    """Test Avatar service health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://avatar:8005/healthz")
        assert response.status_code == 200
        assert response.text.strip() == "healthy"

@pytest.mark.asyncio
async def test_scoring_health():
    """Test Scoring service health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://scoring:8003/healthz")
        assert response.status_code == 200
        assert response.text.strip() == "healthy"

@pytest.mark.asyncio
async def test_all_services_health():
    """Test all services health endpoints"""
    async with httpx.AsyncClient() as client:
        for service in SERVICES:
            response = await client.get(f"http://{service['name']}:{service['port']}/healthz")
            assert response.status_code == 200, f"Service {service['name']} health check failed"
            assert response.text.strip() == "healthy", f"Service {service['name']} returned unexpected response"

def test_imports():
    """Test that all modules can be imported"""
    try:
        import app
        print("✓ Orchestrator imports successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import orchestrator: {e}")

    try:
        import stt.app
        print("✓ STT imports successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import STT: {e}")

    try:
        import llm.app
        print("✓ LLM imports successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import LLM: {e}")

    try:
        import avatar.app
        print("✓ Avatar imports successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import Avatar: {e}")

    try:
        import scoring.app
        print("✓ Scoring imports successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import Scoring: {e}")
