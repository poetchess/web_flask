from functools import wraps

from flask import abort
from flask_login import current_user
from .models import Permission

# For cases in which an entire view function needs to be made available only
# to users with certain permissions, a custom decorator can be used.
# First one for generic permission checks and second one that checks
# specifically for administrator permission.
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)