from flask import jsonify


def print_exception_details(exception_details):
        print(type(exception_details))  # the exception type
        print(exception_details.args)  # arguments stored in .args
        print(exception_details)
        return jsonify(str(type(exception_details)) + " " + str(exception_details.args) + " " + str(exception_details))