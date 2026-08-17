"""
Pytest configuration and fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient for making requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """
    Fixture that resets activities to a known clean state before each test.
    Returns the activities dict and restores it after the test.
    """
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball practice and tournament participation",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis skills development and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["sarah@mergington.edu", "david@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and visual arts techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn and perform instrumental and vocal music",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["avery@mergington.edu", "mason@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Mondays, 4:00 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["isabella@mergington.edu"]
        },
        "Science Lab": {
            "description": "Hands-on experiments and scientific exploration",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        }
    }

    # Clear and reset the activities dict
    activities.clear()
    activities.update(original_activities)

    yield activities

    # Restore original state after test
    activities.clear()
    activities.update(original_activities)
