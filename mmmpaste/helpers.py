from flask import request

def get_ip():
    if not request.headers.get("X-Forwarded-For"):
        return request.remote_addr

    return request.headers.get("X-Forwarded-For")[0]
