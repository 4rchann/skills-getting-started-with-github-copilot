from fastapi.testclient import TestClient

from src.app import activities, app


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
        }
    )


def test_unregister_participant_removes_email():
    reset_activities()
    client = TestClient(app)

    response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")
    assert response.status_code == 200

    response = client.delete("/activities/Chess Club/unregister?email=student@mergington.edu")
    assert response.status_code == 200
    assert "student@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_400():
    reset_activities()
    client = TestClient(app)

    response = client.delete("/activities/Chess Club/unregister?email=ghost@mergington.edu")
    assert response.status_code == 400


def test_activities_response_is_not_cached():
    reset_activities()
    client = TestClient(app)

    response = client.get("/activities")
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "no-store"
