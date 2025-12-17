"""
@author Jack Ringer
Date: 12/16/2025
Description:
Tests for functions in request_processing.py
"""

import pytest
from flask import request
from utils.request_processing import int_check
from werkzeug.exceptions import BadRequest


class TestIntCheck:
    def test_valid_int(self, flask_app):
        with flask_app.test_request_context("/?n=5"):
            result = int_check(request, "n", lower_limit=1, upper_limit=10)
            assert result == 5

    def test_valid_int_post(self, flask_app):
        with flask_app.test_request_context("/", method="POST", json={"n": 5}):
            result = int_check(request, "n", lower_limit=1, upper_limit=10)
            assert result == 5

    def test_missing_value_uses_default(self, flask_app):
        with flask_app.test_request_context("/"):
            result = int_check(request, "n", default_val=7)
            assert result == 7

    def test_missing_value_uses_default_post(self, flask_app):
        with flask_app.test_request_context("/", method="POST", json={}):
            result = int_check(request, "n", default_val=7)
            assert result == 7

    def test_below_lower_limit(self, flask_app):
        with flask_app.test_request_context("/?n=0"):
            with pytest.raises(BadRequest) as exc:
                int_check(request, "n", lower_limit=1)
            assert "must be greater" in str(exc.value)

    def test_below_lower_limit_post(self, flask_app):
        with flask_app.test_request_context("/", method="POST", json={"n": 0}):
            with pytest.raises(BadRequest) as exc:
                int_check(request, "n", lower_limit=1)
            assert "must be greater" in str(exc.value)

    def test_above_upper_limit(self, flask_app):
        with flask_app.test_request_context("/?n=100"):
            with pytest.raises(BadRequest) as exc:
                int_check(request, "n", upper_limit=50)
            assert "must be less" in str(exc.value)

    def test_above_upper_limit_post(self, flask_app):
        with flask_app.test_request_context("/", method="POST", json={"n": 100}):
            with pytest.raises(BadRequest) as exc:
                int_check(request, "n", upper_limit=50)
            assert "must be less" in str(exc.value)

    def test_invalid_type(self, flask_app):
        with flask_app.test_request_context("/?n=foo"):
            with pytest.raises(BadRequest) as exc:
                int_check(request, "n")
            assert "Expected int" in str(exc.value)

    def test_invalid_type_post(self, flask_app):
        with flask_app.test_request_context("/", method="POST", json={"n": "foo"}):
            with pytest.raises(BadRequest) as exc:
                int_check(request, "n")
            assert "Expected int" in str(exc.value)

    def test_zero(self, flask_app):
        with flask_app.test_request_context("/?n=0"):
            result = int_check(request, "n", lower_limit=-10, upper_limit=10)
            assert result == 0

    def test_zero_post(self, flask_app):
        with flask_app.test_request_context("/", method="POST", json={"n": 0}):
            result = int_check(request, "n", lower_limit=-10, upper_limit=10)
            assert result == 0
