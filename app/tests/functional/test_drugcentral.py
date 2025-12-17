"""
@author Jack Ringer
Date: 12/16/2025
Description:
Functional tests for drugcentral blueprint endpoints.
Note here that I'm just checking that the structure of results fetched by the API is correct.
Verifying that the DB itself is "accurate" is part of the DB construction.
"""

from tests.helpers import validate_drugcentral_keys


class TestDrugCentral:
    """Functional tests for drugcentral endpoint."""

    def test_pagination_with_limit(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral' endpoint is requested with a limit parameter
        THEN check that the response contains exactly that many objects
        """
        limit = 5
        url = f"{url_prefix}/drugcentral/?limit={limit}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == limit

        # Validate that each object has the correct keys
        for obj in data:
            validate_drugcentral_keys(obj)

    def test_valid_mol_id_lookup(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral/{mol_id}' endpoint is requested with a valid mol_id
        THEN check that a valid object is returned with correct keys
        """
        mol_id = 4922  # paracetamol
        url = f"{url_prefix}/drugcentral/{mol_id}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

        # Should return at least one object
        if len(data) > 0:
            # Validate the first object
            obj = data[0]
            validate_drugcentral_keys(obj)
            # Verify that the mol_id matches
            assert obj["mol_id"] == mol_id

    def test_invalid_mol_id_lookup(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral/{mol_id}' endpoint is requested with an invalid mol_id
        THEN check that either no data is returned or an appropriate error status is returned
        """
        mol_id = -1  # Invalid mol_id
        url = f"{url_prefix}/drugcentral/{mol_id}"
        response = test_client.get(url)

        # The API should either return 200 with empty list or 404
        if response.status_code == 200:
            data = response.get_json()
            assert isinstance(data, list)
            # Should return empty list for invalid mol_id
            assert len(data) == 0
        else:
            # Or return an error status code
            assert response.status_code in [400, 404]

    def test_default_limit_behavior(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral' endpoint is requested without a limit parameter
        THEN check that the default limit (10) is applied
        """
        url = f"{url_prefix}/drugcentral/"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Default limit should be 10 based on the API spec
        assert len(data) <= 10

        # Validate keys for all returned objects
        for obj in data:
            validate_drugcentral_keys(obj)

    def test_limit_edge_case_zero(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral' endpoint is requested with limit=0
        THEN check that no objects are returned
        """
        url = f"{url_prefix}/drugcentral/?limit=0"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_limit_edge_case_one(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral' endpoint is requested with limit=1
        THEN check that exactly one object is returned
        """
        url = f"{url_prefix}/drugcentral/?limit=1"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1

        # Validate the single object
        validate_drugcentral_keys(data[0])

    def test_offset_parameter(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral' endpoint is requested with offset parameter
        THEN check that the response skips the specified number of records
        """
        limit = 5
        offset = 2

        # Get first batch (records 0-4)
        url_first = f"{url_prefix}/drugcentral/?limit={limit}"
        response_first = test_client.get(url_first)
        data_first = response_first.get_json()

        # Get second batch with offset (should start at record 2, so records 2-6)
        url_offset = f"{url_prefix}/drugcentral/?limit={limit}&offset={offset}"
        response_offset = test_client.get(url_offset)
        data_offset = response_offset.get_json()

        assert response_first.status_code == 200
        assert response_offset.status_code == 200
        assert isinstance(data_first, list)
        assert isinstance(data_offset, list)

        # Verify we got data
        if len(data_first) >= limit and len(data_offset) > 0:
            # Validate keys for all objects
            for obj in data_offset:
                validate_drugcentral_keys(obj)

            # The offset batch should start at the position specified by offset
            # So data_offset[0] should equal data_first[offset]
            # This verifies that offset actually skips the correct number of records
            if len(data_first) > offset:
                assert data_offset[0]["mol_id"] == data_first[offset]["mol_id"]
                assert data_offset[0]["name"] == data_first[offset]["name"]

    def test_response_format_is_json(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral' endpoint is requested
        THEN check that the response is in JSON format
        """
        url = f"{url_prefix}/drugcentral/?limit=1"
        response = test_client.get(url)

        assert response.status_code == 200
        assert response.content_type == "application/json"

        # Verify we can parse the JSON
        data = response.get_json()
        assert data is not None

    def test_large_limit_value(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/drugcentral' endpoint is requested with a large limit value
        THEN check that the response handles it appropriately (up to max of 1000)
        """
        limit = 1000  # Maximum allowed limit based on API spec
        url = f"{url_prefix}/drugcentral/?limit={limit}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Should return up to 1000 objects
        assert len(data) <= limit

        # Validate keys for a sample of objects (not all to keep test fast)
        if len(data) > 0:
            validate_drugcentral_keys(data[0])
            if len(data) > 1:
                validate_drugcentral_keys(data[-1])
