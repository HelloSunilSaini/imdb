from functools import wraps

from flask import request, session, current_app as app
from flask_restful import Resource

headers_mapping = {
    'csv': {'content-type': 'application/csv'},
    'json': {'content-type': 'application/json'},
}


def ok_response(response, message="OK", headers='json'):
    return True, response, 200, message, headers_mapping[headers]


def error_response(code, message, headers='json', response={}):
    return False, response, code, message, headers_mapping[headers]


def sanitize_response(response):
    data = None
    status = 200
    headers = {}

    if isinstance(response, tuple) and len(response) is 3:
        data, status, headers = response
    if isinstance(response, tuple) and len(response) is 5:
        status, data, code, message, header = response
        return status, data, code, message, headers.update(header)
    else:
        data = response
    return data, status, headers


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)
        if session.get('user_id', False):
            return func(*args, **kwargs)

        app.logger.error("Unauthorized request from %s", request.remote_addr)
        return False, {}, 401, 'Unauthorized', {'Content-Type': 'application/json'}

    return wrapper



def patch_response_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = sanitize_response(func(*args, **kwargs))
        if isinstance(response, tuple) and len(response) is 5:
            status, data, code, message, headers = response
            data = {"responseData": data,
                    "status": status,
                    "message": message}

            return data, code, headers
        else:
            if not getattr(func, 'sanitize_response', True):
                resp = func(*args, **kwargs)
                resp.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return resp
            data, status, headers = response
        patched = isinstance(data, dict) and (
            "errorCode" in data or "responseData" in data
        )

        if not patched:
            data = {
                "responseData": data
            }

        if 'errorCode' in list(data.keys()):
            status = data['errorCode']

        return data, status, headers

    return wrapper


def cors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data, status, headers = sanitize_response(func(*args, **kwargs))

        headers.update({
            'Access-Control-Allow-Headers': ', '.join(app.config.get('CORS_ALLOW_HEADERS', [])),
            'Access-Control-Allow-Origin':  ', '.join(app.config.get('CORS_ALLOW_ORIGINS', [])),
            'Access-Control-Allow-Methods': ', '.join(app.config.get('CORS_ALLOW_METHODS', []))
        })

        return data, status, headers

    return wrapper


class Resource(Resource):
    def options(self, **kwargs):
        app.logger.info("Obtained options request from %s", request.remote_addr)
        return "OK"
    options.authenticated = False

    method_decorators = [
        authenticate,
        # Keep it in the end
        patch_response_data
    ]
