"""
@author Jack Ringer
Date: 10/2/2024
Description:
Utilities related to type-checking user input.
"""

from flask import abort


def int_check(n, var_name: str):
    try:
        n = int(n)
    except:
        return abort(400, f"Invalid {var_name} provided. Expected int but got: {n}")
    return n
