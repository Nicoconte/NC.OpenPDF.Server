from functools import wraps

from api.common.utils.token import ( 
    get_token_from_request,
    get_user_by_token
)

def init_storage(storage, function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        token = get_token_from_request(request)
        user  = get_user_by_token(token)
        
        storage.init(user.username)

        return function(request, *args, **kwargs)

    return decorator