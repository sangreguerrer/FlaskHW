import json


def get_http_error(error_class, message):
    return error_class(                        
        text=json.dumps({"error": message}),   
        content_type='application/json')