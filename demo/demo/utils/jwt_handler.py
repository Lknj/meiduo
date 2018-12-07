from rest_framework_jwt.utils import jwt_response_payload_handler
from rest_framework_jwt.utils import jwt_payload_handler


def jwt_response_handler(token, user=None, request=None):
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }

def jwt_payload_handler2(user):
    payload = jwt_payload_handler(user)
    if 'email' in payload:
        del payload['email']
    payload['mobile'] = user.mobile
    return payload