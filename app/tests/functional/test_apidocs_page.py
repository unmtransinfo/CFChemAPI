"""
@author Jack Ringer
Date: 12/16/2025
Description:
Simple test to verify 200 response from /apidocs page
"""


def test_apidocs_page(test_client):
    """
    GIVEN a Flask/Flasger application configured for testing
    WHEN the '/apidocs' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/apidocs/")
    assert response.status_code == 200
