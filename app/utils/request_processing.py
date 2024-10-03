"""
@author Jack Ringer
Date: 8/3/2024
Description:
Functions related to parsing requests.
"""

from flask import abort


def process_list_input(request, param_name: str, limit: int):
    value_list = request.args.get(param_name, type=str)
    if not value_list:
        return abort(400, f"No {param_name} provided")
    value_list = value_list.split(",")
    if len(value_list) > limit:
        return abort(
            400,
            f"Provided list of {param_name} exceeded limit of {limit}. Please provide <= {limit} {param_name} at a time.",
        )
    return value_list


def process_integer_list_input(request, param_name: str, limit):
    int_list = process_list_input(request, param_name, limit)
    try:
        int_list = [int(cid) for cid in int_list]
    except ValueError:
        return abort(
            400,
            f"Provided list of {param_name} contains non-integer elements. Please check input.",
        )
    return int_list
