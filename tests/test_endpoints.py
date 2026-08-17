"""
Integration tests for all FastAPI endpoints.
Tests the complete request/response flow for activities API.
"""

from urllib.parse import quote
import pytest
from tests.test_fixtures import (
    SAMPLE_EMAIL,
    SAMPLE_EMAIL_WITH_TAG,
    SAMPLE_EMAIL_INTERNATIONAL,
)


class TestGetActivitiesEndpoint:
    """Test GET /activities endpoint."""

    def test_get_activities_returns_200(self, client, clean_activities):
        """Test that GET /activities returns successful response."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client, clean_activities):
        """Test that endpoint returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_all_activities(self, client, clean_activities):
        """Test that response contains all expected activities."""
        response = client.get("/activities")
        activities = response.json()
        
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Debate Club",
            "Science Lab",
        ]
        
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_structure(self, client, clean_activities):
        """Test that each activity has correct structure."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participant_counts(self, client, clean_activities):
        """Test that activities have correct initial participant counts."""
        response = client.get("/activities")
        activities = response.json()
        
        # Verify Chess Club has 2 participants
        assert len(activities["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


class TestSignupEndpoint:
    """Test POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, clean_activities):
        """Test successful signup to an activity."""
        response = client.post(
            "/activities/Art%20Studio/signup?email=newstudent@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_updates_participants_list(self, client, clean_activities):
        """Test that signup actually adds student to participants."""
        email = "newstudent@mergington.edu"
        client.post(
            f"/activities/Art%20Studio/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Art Studio"]["participants"]

    def test_signup_duplicate_student_error(self, client, clean_activities):
        """Test that signup fails for already registered student."""
        email = "michael@mergington.edu"
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_full_error(self, client, clean_activities):
        """Test that signup fails when activity is at capacity."""
        # Basketball Team has max_participants=15 and 1 participant (james@mergington.edu)
        # We need to fill it up to test the full activity error
        response = client.get("/activities")
        activities = response.json()
        
        # Gym Class has max_participants=30 and 2 participants
        # Let's create a scenario with a nearly full activity
        # First, get a fresh activity with limited capacity
        
        # Programming Class has max_participants=20 with 2 participants
        # Add 18 more to fill it up
        for i in range(18):
            client.post(
                f"/activities/Programming%20Class/signup?email=student{i}@mergington.edu",
                headers={"Content-Type": "application/json"}
            )
        
        # Now try to signup another student - should fail
        response = client.post(
            "/activities/Programming%20Class/signup?email=fullstudent@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()

    def test_signup_nonexistent_activity_error(self, client, clean_activities):
        """Test that signup fails for non-existent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup?email=student@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_with_special_character_email(self, client, clean_activities):
        """Test signup with email containing special characters."""
        response = client.post(
            f"/activities/Art%20Studio/signup?email={quote(SAMPLE_EMAIL_WITH_TAG)}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        # Verify it was added correctly
        get_response = client.get("/activities")
        activities = get_response.json()
        assert SAMPLE_EMAIL_WITH_TAG in activities["Art Studio"]["participants"]

    def test_signup_with_international_email(self, client, clean_activities):
        """Test signup with international domain email."""
        response = client.post(
            f"/activities/Music%20Band/signup?email={SAMPLE_EMAIL_INTERNATIONAL}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        # Verify it was added correctly
        get_response = client.get("/activities")
        activities = get_response.json()
        assert SAMPLE_EMAIL_INTERNATIONAL in activities["Music Band"]["participants"]

    def test_signup_with_activity_name_with_spaces(self, client, clean_activities):
        """Test signup with activity name containing spaces."""
        response = client.post(
            "/activities/Basketball%20Team/signup?email=baller@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200

    def test_signup_multiple_students_same_activity(self, client, clean_activities):
        """Test that multiple students can signup for same activity."""
        emails = ["student1@test.com", "student2@test.com", "student3@test.com"]
        
        for email in emails:
            response = client.post(
                f"/activities/Debate%20Club/signup?email={email}",
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200
        
        # Verify all were added
        get_response = client.get("/activities")
        activities = get_response.json()
        for email in emails:
            assert email in activities["Debate Club"]["participants"]


class TestUnregisterEndpoint:
    """Test POST /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client, clean_activities):
        """Test successful unregister from activity."""
        email = "michael@mergington.edu"
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_removes_participant(self, client, clean_activities):
        """Test that unregister actually removes student from participants."""
        email = "michael@mergington.edu"
        
        # Verify student is registered
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]
        
        # Unregister
        client.post(
            f"/activities/Chess%20Club/unregister?email={email}",
            headers={"Content-Type": "application/json"}
        )
        
        # Verify student is removed
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities["Chess Club"]["participants"]

    def test_unregister_not_registered_error(self, client, clean_activities):
        """Test that unregister fails for non-registered student."""
        email = "notregistered@mergington.edu"
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_unregister_nonexistent_activity_error(self, client, clean_activities):
        """Test that unregister fails for non-existent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/unregister?email=student@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_creates_available_spot(self, client, clean_activities):
        """Test that unregistering a student frees up a spot."""
        # First, get initial participant count for Programming Class
        response = client.get("/activities")
        activities = response.json()
        initial_count = len(activities["Programming Class"]["participants"])
        
        # Unregister a student
        email = "emma@mergington.edu"
        client.post(
            f"/activities/Programming%20Class/unregister?email={email}",
            headers={"Content-Type": "application/json"}
        )
        
        # Verify count decreased
        response = client.get("/activities")
        activities = response.json()
        new_count = len(activities["Programming Class"]["participants"])
        assert new_count == initial_count - 1

    def test_unregister_allows_new_signup(self, client, clean_activities):
        """Test that after unregister, a new student can take the spot."""
        # Fill up a small activity first
        # Basketball Team: max=15, has 1 participant (james@mergington.edu)
        # Add 14 more to fill it
        for i in range(14):
            client.post(
                f"/activities/Basketball%20Team/signup?email=player{i}@mergington.edu",
                headers={"Content-Type": "application/json"}
            )
        
        # Try to add another - should fail (at capacity)
        response = client.post(
            "/activities/Basketball%20Team/signup?email=extra@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        
        # Unregister one student
        client.post(
            "/activities/Basketball%20Team/unregister?email=james@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        
        # Now signup should succeed
        response = client.post(
            "/activities/Basketball%20Team/signup?email=extra@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200


class TestRootEndpoint:
    """Test GET / endpoint (root redirect)."""

    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]

    def test_root_redirect_follows(self, client):
        """Test that following redirect works."""
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
