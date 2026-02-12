"""Tests for getting activities"""
import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Soccer Team" in data


def test_get_activities_structure(client):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    assert isinstance(activity["participants"], list)
    assert isinstance(activity["max_participants"], int)


def test_get_activities_participants(client):
    """Test that participants are correctly loaded"""
    response = client.get("/activities")
    data = response.json()
    
    # Chess Club should have 2 participants
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    
    # Soccer Team should have 0 participants
    assert len(data["Soccer Team"]["participants"]) == 0
