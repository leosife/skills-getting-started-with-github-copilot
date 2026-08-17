"""
Test fixtures and helper functions for the activity signup system tests.
"""


# Sample test data
SAMPLE_ACTIVITY_DATA = {
    "name": "Test Activity",
    "description": "A test activity for validation",
    "schedule": "Mondays, 3:00 PM - 4:00 PM",
    "max_participants": 5,
    "participants": []
}

SAMPLE_EMAIL = "test@mergington.edu"
SAMPLE_EMAIL_WITH_TAG = "test+tag@mergington.edu"
SAMPLE_EMAIL_INTERNATIONAL = "test@example.co.uk"

ACTIVITY_WITH_CAPACITY = {
    "description": "Full activity",
    "schedule": "Mondays, 3:00 PM - 4:00 PM",
    "max_participants": 2,
    "participants": ["user1@mergington.edu", "user2@mergington.edu"]
}

ACTIVITY_WITH_ONE_SPOT = {
    "description": "Almost full activity",
    "schedule": "Mondays, 3:00 PM - 4:00 PM",
    "max_participants": 2,
    "participants": ["user1@mergington.edu"]
}

ACTIVITY_NAMES_WITH_SPECIAL_CHARS = [
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Basketball Team",
    "Test & Demo",
]


def verify_activity_structure(activity_dict):
    """
    Verify that an activity dict has the correct structure.
    
    Args:
        activity_dict: Dictionary to validate
        
    Returns:
        bool: True if structure is valid, False otherwise
    """
    required_keys = {"description", "schedule", "max_participants", "participants"}
    if not isinstance(activity_dict, dict):
        return False
    if not required_keys.issubset(activity_dict.keys()):
        return False
    if not isinstance(activity_dict["participants"], list):
        return False
    if not isinstance(activity_dict["max_participants"], int):
        return False
    if activity_dict["max_participants"] <= 0:
        return False
    return True


def get_available_spots(activity_dict):
    """
    Calculate the number of available spots in an activity.
    
    Args:
        activity_dict: Activity dictionary
        
    Returns:
        int: Number of available spots
    """
    return activity_dict["max_participants"] - len(activity_dict["participants"])


def is_activity_full(activity_dict):
    """
    Check if an activity is at capacity.
    
    Args:
        activity_dict: Activity dictionary
        
    Returns:
        bool: True if activity is full, False otherwise
    """
    return len(activity_dict["participants"]) >= activity_dict["max_participants"]


def email_is_registered(activity_dict, email):
    """
    Check if an email is already registered for an activity.
    
    Args:
        activity_dict: Activity dictionary
        email: Email to check
        
    Returns:
        bool: True if email is in participants list, False otherwise
    """
    return email in activity_dict["participants"]
