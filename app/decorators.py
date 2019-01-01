from dropbox.exceptions import (
    ApiError, BadInputError, AuthError, InternalServerError,
    RateLimitError,
)
from flask import jsonify


def get_d_box_exception_tuple():
    return (
        ApiError, BadInputError, AuthError, InternalServerError,
        RateLimitError
    )


def d_box_catch_exceptions(call_back):
    def call_back_wrapper(*args, **kwargs):
        try:
            call_back_results = call_back(*args, **kwargs)
        except get_d_box_exception_tuple() as e:
            return {'errors': repr(e)}
        except Exception as e:
            return {'errors': repr(e)}
        else:
            return call_back_results

    return call_back_wrapper
