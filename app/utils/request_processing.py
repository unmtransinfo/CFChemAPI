"""
@author Jack Ringer
Date: 10/31/2025
Description:
Functions related to parsing requests.
"""

from typing import Union

from flask import abort


def _method_not_supported(request):
    return abort(405, f"Method {request.method} not supported")


def get_param(request, param_name: str, type, default_val=None):
    val = None
    if request.method == "GET":
        val = request.args.get(param_name, type=type)
    elif request.method == "POST":
        val = request.json.get(param_name)
    else:
        return _method_not_supported(request)
    if val is None:
        val = default_val
    return val


def int_check(
    request,
    var_name: str,
    lower_limit: Union[None, int] = None,
    upper_limit: Union[None, int] = None,
    default_val: Union[None, int] = None,
):
    n = get_param(request, var_name, type=int, default_val=default_val)
    try:
        n = int(n)
    except:
        return abort(
            400,
            f"Invalid {var_name} provided. Expected int but got: {request.args.get(var_name)}",
        )
    if lower_limit is not None and n < lower_limit:
        return abort(400, f"Error: {var_name} must be greater than {lower_limit}")
    if upper_limit is not None and n > upper_limit:
        return abort(400, f"Error: {var_name} must be less than {upper_limit}")
    return n
