import json
import traceback
from datetime import datetime
from django.db import close_old_connections, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, PermissionDenied, ValidationError
from flask import request
from imdb.utils.logger import get_root_logger
from imdb.utils.custom_error import CustomError
from imdb.utils.resource import error_response

logger = get_root_logger()


def parse_request_for_error(request_obj):

    try:
        request_headers = "Headers: " + json.dumps(dict(request.headers)) + "\n"
    except Exception as e:
        logger.exception(e)
        request_headers = ''

    try:
        request_params = "Params: " + json.dumps(request_obj.args.to_dict()) + "\n"
    except Exception as e:
        logger.exception(e)
        request_params = ''

    try:
        request_json = "JSON: " + json.dumps(request.get_json(force=True)) + "\n"
    except Exception as e:
        logger.exception(e)
        request_json = ''

    request_parsed = '\n'.join([request_headers, request_params, request_json])

    return request_parsed


class ErrorHandler(object):

    def __init__(self, api_key):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.api_key = api_key

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def wrapped_f(*args, **kwargs):
            try:
                start = datetime.now()
                output = f(*args, **kwargs)
                logger.info("Time taken for %s is %s", self.api_key, datetime.now() - start)
                return output
            except KeyError as e:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API:\n%s Request: \n%s", self.api_key, exception_trace, parsed_request)
                logger.error("Missing key : " + e.__repr__())
                return error_response(400, "{} is required".format(e.__repr__()))
            except (ValidationError, TypeError) as e:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API:\n%s Request: \n%s", self.api_key, exception_trace, parsed_request)
                logger.error("Missing key : " + e.__repr__())
                return error_response(400, "Bad Request object. Missing Parameters or wrong endpoint")
            except ValueError as e:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API:\n%s Request: \n%s", self.api_key, exception_trace, parsed_request)
                logger.error("Missing key : " + e.__repr__())
                return error_response(400, "Bad Request. Incorrect Parameter types")
            except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API:\n%s Request: \n%s", self.api_key, exception_trace, parsed_request)
                logger.error("Missing key : " + e.__repr__())
                return error_response(422, "Unprocessable Entity, no records found or multiple records found")
            except PermissionDenied as e:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API:\n%s Request: \n%s", self.api_key, exception_trace, parsed_request)
                logger.error("Missing key : " + e.__repr__())
                return error_response(403, "Permission Denied")
            except CustomError as error:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API: %s\n%s \nRequest: %s", self.api_key, error.get_message(),
                             exception_trace, parsed_request)
                return error_response(error.get_error_code(), error.get_message())
            except IntegrityError as e:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API:\n%s Request: \n%s", self.api_key, exception_trace, parsed_request)
                db_err_code, _ = e.args
                if db_err_code == 1062:
                    return error_response(400, "Duplicate Entry")
                return error_response(500, "Internal Server Error")
            except Exception as e:
                exception_trace = traceback.format_exc()
                parsed_request = parse_request_for_error(request)
                logger.error("Exception in %s API:\n%s Request: \n%s", self.api_key, exception_trace, parsed_request)
                logger.error("Missing key : " + e.__repr__())
                return error_response(500, "Internal Server Error")
            finally:
                close_old_connections()
        return wrapped_f
