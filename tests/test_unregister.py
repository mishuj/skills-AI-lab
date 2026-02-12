"""Tests for unregistering from activities"""
import pytest


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    response = client.post(
        "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    # Verify participant is there
    response = client.get("/activities")
    assert "michael@mergington.edu" in response.json()["Chess Club"]["participants"]
    
    # Unregister
    client.post("/activities/Chess%20Club/unregister?email=michael@mergington.edu")
    
    # Verify participant is removed
    response = client.get("/activities")
    assert "michael@mergington.edu" not in response.json()["Chess Club"]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister returns 404 for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent%20Activity/unregister?email=john@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_signed_up(client):
    """Test that unregister fails if student is not signed up"""
    response = client.post(
        "/activities/Soccer%20Team/unregister?email=notmember@mergington.edu"
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_then_signup_again(client):
    """Test that a student can sign up again after unregistering"""
    email = "michael@mergington.edu"
    activity = "Chess%20Club"
    
    # Unregister
    response1 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 200
    
    # Verify signup
    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]


def test_unregister_multiple_participants(client):
    """Test unregistering one of multiple participants"""
    # Sign up additional students
    client.post("/activities/Chess%20Club/signup?email=alice@mergington.edu")
    client.post("/activities/Chess%20Club/signup?email=bob@mergington.edu")
    
    # Verify all are there
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert len(participants) == 4
    
    # Unregister one
    client.post("/activities/Chess%20Club/unregister?email=alice@mergington.edu")
    
    # Verify only alice was removed
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert len(participants) == 3
    assert "alice@mergington.edu" not in participants
    assert "bob@mergington.edu" in participants
    assert "michael@mergington.edu" in participants
