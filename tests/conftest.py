"""
Test Configuration and Fixtures
================================
Pytest fixtures и конфигурация для тестирования приложения.
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from app import create_app


@pytest.fixture
def app():
    """
    Create and configure a test Flask app instance.
    
    Yields:
        Flask app configured for testing
    """
    app = create_app(config_name='testing')
    app.config['TESTING'] = True
    
    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the app.
    
    Args:
        app: Flask app fixture
        
    Returns:
        Flask test client
    """
    return app.test_client()


@pytest.fixture
def app_context(app):
    """
    Create an application context for testing.
    
    Args:
        app: Flask app fixture
        
    Yields:
        Flask application context
    """
    with app.app_context():
        yield app
