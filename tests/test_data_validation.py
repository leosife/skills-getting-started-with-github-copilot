"""
Unit tests for data validation functions and activity structure verification.
"""

import pytest
from tests.test_fixtures import (
    verify_activity_structure,
    get_available_spots,
    is_activity_full,
    email_is_registered,
    SAMPLE_ACTIVITY_DATA,
    SAMPLE_EMAIL,
    ACTIVITY_WITH_CAPACITY,
    ACTIVITY_WITH_ONE_SPOT,
)


class TestActivityStructureValidation:
    """Test verify_activity_structure helper function."""

    def test_valid_activity_structure(self):
        """Test that a properly structured activity passes validation."""
        assert verify_activity_structure(SAMPLE_ACTIVITY_DATA) is True

    def test_valid_activity_with_participants(self):
        """Test validation of activity with existing participants."""
        assert verify_activity_structure(ACTIVITY_WITH_CAPACITY) is True

    def test_invalid_non_dict(self):
        """Test that non-dict input fails validation."""
        assert verify_activity_structure("not a dict") is False
        assert verify_activity_structure(None) is False
        assert verify_activity_structure([]) is False

    def test_invalid_missing_required_keys(self):
        """Test that missing required keys fail validation."""
        incomplete = {"description": "Test", "schedule": "Monday"}
        assert verify_activity_structure(incomplete) is False

    def test_invalid_participants_not_list(self):
        """Test that non-list participants field fails validation."""
        invalid = SAMPLE_ACTIVITY_DATA.copy()
        invalid["participants"] = "not a list"
        assert verify_activity_structure(invalid) is False

    def test_invalid_max_participants_not_int(self):
        """Test that non-int max_participants fails validation."""
        invalid = SAMPLE_ACTIVITY_DATA.copy()
        invalid["max_participants"] = "20"
        assert verify_activity_structure(invalid) is False

    def test_invalid_zero_max_participants(self):
        """Test that zero max_participants fails validation."""
        invalid = SAMPLE_ACTIVITY_DATA.copy()
        invalid["max_participants"] = 0
        assert verify_activity_structure(invalid) is False

    def test_invalid_negative_max_participants(self):
        """Test that negative max_participants fails validation."""
        invalid = SAMPLE_ACTIVITY_DATA.copy()
        invalid["max_participants"] = -5
        assert verify_activity_structure(invalid) is False


class TestAvailableSpots:
    """Test get_available_spots helper function."""

    def test_available_spots_with_no_participants(self):
        """Test available spots calculation with empty activity."""
        assert get_available_spots(SAMPLE_ACTIVITY_DATA) == 5

    def test_available_spots_with_participants(self):
        """Test available spots calculation with existing participants."""
        assert get_available_spots(ACTIVITY_WITH_ONE_SPOT) == 1

    def test_available_spots_activity_full(self):
        """Test available spots when activity is at capacity."""
        assert get_available_spots(ACTIVITY_WITH_CAPACITY) == 0

    def test_available_spots_large_capacity(self):
        """Test available spots with large capacity activity."""
        activity = {
            "description": "Big class",
            "schedule": "Monday",
            "max_participants": 100,
            "participants": ["user@example.com"]
        }
        assert get_available_spots(activity) == 99


class TestActivityFullCheck:
    """Test is_activity_full helper function."""

    def test_activity_not_full_empty(self):
        """Test that empty activity is not full."""
        assert is_activity_full(SAMPLE_ACTIVITY_DATA) is False

    def test_activity_not_full_with_space(self):
        """Test that activity with space is not full."""
        assert is_activity_full(ACTIVITY_WITH_ONE_SPOT) is False

    def test_activity_full(self):
        """Test that activity at capacity is full."""
        assert is_activity_full(ACTIVITY_WITH_CAPACITY) is True

    def test_activity_full_with_multiple_participants(self):
        """Test activity full with various participant counts."""
        activity = {
            "description": "Test",
            "schedule": "Monday",
            "max_participants": 3,
            "participants": ["a@test.com", "b@test.com", "c@test.com"]
        }
        assert is_activity_full(activity) is True


class TestEmailRegistration:
    """Test email_is_registered helper function."""

    def test_email_not_registered_empty_list(self):
        """Test email not registered when participants list is empty."""
        assert email_is_registered(SAMPLE_ACTIVITY_DATA, SAMPLE_EMAIL) is False

    def test_email_registered(self):
        """Test email correctly identified as registered."""
        activity = {
            "description": "Test",
            "schedule": "Monday",
            "max_participants": 10,
            "participants": [SAMPLE_EMAIL]
        }
        assert email_is_registered(activity, SAMPLE_EMAIL) is True

    def test_email_not_registered_other_emails_present(self):
        """Test email not registered when other emails exist."""
        activity = {
            "description": "Test",
            "schedule": "Monday",
            "max_participants": 10,
            "participants": ["other@test.com", "another@test.com"]
        }
        assert email_is_registered(activity, SAMPLE_EMAIL) is False

    def test_email_case_sensitive(self):
        """Test that email check is case-sensitive."""
        activity = {
            "description": "Test",
            "schedule": "Monday",
            "max_participants": 10,
            "participants": ["Test@example.com"]
        }
        assert email_is_registered(activity, "test@example.com") is False
        assert email_is_registered(activity, "Test@example.com") is True

    def test_email_with_special_characters(self):
        """Test email registration with special characters."""
        activity = {
            "description": "Test",
            "schedule": "Monday",
            "max_participants": 10,
            "participants": ["test+tag@example.com"]
        }
        assert email_is_registered(activity, "test+tag@example.com") is True
        assert email_is_registered(activity, "test@example.com") is False
