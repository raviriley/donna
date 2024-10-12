# import os
# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import patch
# from backend.main import app

# client = TestClient(app)

# @pytest.fixture
# def mock_twilio_client():
#     with patch("backend.main.get_twilio_client") as mock:
#         yield mock

# def test_trigger_outbound_call(mock_twilio_client):
#     # Arrange
#     mock_twilio_instance = mock_twilio_client.return_value
#     mock_twilio_instance.calls.create.return_value.sid = "CA1234567890abcdef"

#     payload = {
#         "phone_number": "+1234567890"
#     }

#     # Act
#     response = client.post("/calls/outbound", json=payload)

#     # Assert
#     assert response.status_code == 200
#     assert response.json() == {
#         "message": "Call initiated! Call SID: CA1234567890abcdef",
#         "twilio_call_sid": "CA1234567890abcdef",
#     }
#     mock_twilio_instance.calls.create.assert_called_once()
