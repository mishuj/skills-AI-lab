"""Tests for signing up for activities"""
import pytest


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Soccer%20Team/signup?email=john@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "john@mergington.edu" in data["message"]
    assert "Soccer Team" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds the participant"""
    # Sign up
    client.post("/activities/Soccer%20Team/signup?email=new@mergington.edu")
    
    # Verify signup
    response = client.get("/activities")
    data = response.json()
    assert "new@mergington.edu" in data["Soccer Team"]["participants"]


def test_signup_activity_not_found(client):
    """Test signup returns 404 for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent%20Activity/signup?email=john@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_signed_up(client):
    """Test that a student cannot sign up twice"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_different_students_same_activity(client):
    """Test that multiple different students can sign up for the same activity"""
    # First signup
    response1 = client.post(
        "/activities/Soccer%20Team/signup?email=student1@mergington.edu"
    )
    assert response1.status_code == 200
    
    # Second signup
    response2 = client.post(
        "/activities/Soccer%20Team/signup?email=student2@mergington.edu"
    )
    assert response2.status_code == 200
    
    # Verify both are signed up
    response = client.get("/activities")
    data = response.json()
    participants = data["Soccer Team"]["participants"]
    assert "student1@mergington.edu" in participants
    assert "student2@mergington.edu" in participants
    assert len(participants) == 2


def test_signup_same_student_different_activities(client):
    """Test that the same student can sign up for multiple activities"""
    email = "student@mergington.edu"
    
    # Sign up for Soccer Team
    response1 = client.post(
        "/activities/Soccer%20Team/signup?email=" + email
    )
    assert response1.status_code == 200
    
    # Sign up for Chess Club
    response2 = client.post(
        "/activities/Chess%20Club/signup?email=" + email
    )
    assert response2.status_code == 200
    
    # Verify signup in both activities
    response = client.get("/activities")
    data = response.json()
    assert email in data["Soccer Team"]["participants"]
    assert email in data["Chess Club"]["participants"]
