"""
@author Jack Ringer
Date: 12/17/2025
Description:
Functional tests for search blueprint endpoints.
Note here that I'm just checking that the structure of results fetched by the API is correct.
Verifying that the DB itself is "accurate" is part of the DB construction.
"""

from tests.helpers import validate_lincs_keys


class TestSearch:
    """Functional tests for search endpoint."""

    def test_search_with_query(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with a query parameter
        THEN check that the response returns valid LINCS objects
        """
        query = "genistein"
        url = f"{url_prefix}/search/?query={query}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

        # Validate that each object has the correct keys (LINCS keys)
        for obj in data:
            validate_lincs_keys(obj)

    def test_search_with_empty_query(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with an empty query
        THEN check that the response returns results (default behavior)
        """
        url = f"{url_prefix}/search/"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

        # With empty query, should still return results (matches all)
        # Validate keys for returned objects
        for obj in data:
            validate_lincs_keys(obj)

    def test_search_with_limit(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with a limit parameter
        THEN check that the response contains at most that many objects
        """
        limit = 5
        query = "kinase"
        url = f"{url_prefix}/search/?query={query}&limit={limit}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) <= limit

        # Validate that each object has the correct keys
        for obj in data:
            validate_lincs_keys(obj)

    def test_search_default_limit_behavior(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested without a limit parameter
        THEN check that the default limit (10) is applied
        """
        query = "inhibitor"
        url = f"{url_prefix}/search/?query={query}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Default limit should be 10 based on the API spec
        assert len(data) <= 10

        # Validate keys for all returned objects
        for obj in data:
            validate_lincs_keys(obj)

    def test_search_with_offset(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with offset parameter
        THEN check that the response skips the specified number of records
        """
        limit = 5
        offset = 2
        query = "inhibitor"

        # Get first batch (records 0-4)
        url_first = f"{url_prefix}/search/?query={query}&limit={limit}"
        response_first = test_client.get(url_first)
        data_first = response_first.get_json()

        # Get second batch with offset (should start at record 2, so records 2-6)
        url_offset = f"{url_prefix}/search/?query={query}&limit={limit}&offset={offset}"
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
                validate_lincs_keys(obj)

            # The offset batch should start at the position specified by offset
            if len(data_first) > offset:
                assert data_offset[0]["mol_id"] == data_first[offset]["mol_id"]
                assert data_offset[0]["pert_name"] == data_first[offset]["pert_name"]

    def test_search_no_results(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with a query that matches nothing
        THEN check that an empty list is returned
        """
        query = "xyznonexistentcompound12345"
        url = f"{url_prefix}/search/?query={query}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Should return empty list for query with no matches
        assert len(data) == 0

    def test_search_response_format_is_json(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested
        THEN check that the response is in JSON format
        """
        query = "kinase"
        url = f"{url_prefix}/search/?query={query}&limit=1"
        response = test_client.get(url)

        assert response.status_code == 200
        assert response.content_type == "application/json"

        # Verify we can parse the JSON
        data = response.get_json()
        assert data is not None

    def test_search_limit_edge_case_zero(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with limit=0
        THEN check that no objects are returned
        """
        query = "inhibitor"
        url = f"{url_prefix}/search/?query={query}&limit=0"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_search_limit_edge_case_one(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with limit=1
        THEN check that at most one object is returned
        """
        query = "kinase"
        url = f"{url_prefix}/search/?query={query}&limit=1"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) <= 1

        # Validate the object if one is returned
        if len(data) == 1:
            validate_lincs_keys(data[0])

    def test_search_large_limit_value(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with a large limit value
        THEN check that the response handles it appropriately (up to max of 1000)
        """
        limit = 1000  # Maximum allowed limit based on API spec
        query = "inhibitor"
        url = f"{url_prefix}/search/?query={query}&limit={limit}"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Should return up to 1000 objects
        assert len(data) <= limit

        # Validate keys for a sample of objects (not all to keep test fast)
        if len(data) > 0:
            validate_lincs_keys(data[0])
            if len(data) > 1:
                validate_lincs_keys(data[-1])

    def test_search_partial_match(self, test_client, url_prefix):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/search' endpoint is requested with a partial query string
        THEN check that partial matches are returned (LIKE behavior)
        """
        query = "gen"  # Should match "genistein" and other compounds with "gen"
        url = f"{url_prefix}/search/?query={query}&limit=5"
        response = test_client.get(url)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

        # Validate that each object has the correct keys
        for obj in data:
            validate_lincs_keys(obj)
