from functools import wraps
from flask_login import current_user
from flask import redirect

from app.models import UserRole


def annonymous_user(f):
    @wraps(f)
    def decorated_func(*args,**kwargs):
        if current_user.is_authenticated:
            return redirect("/")
        return f(*args,**kwargs)

    return decorated_func

def annonymous_employee(f):
    @wraps(f)
    def auth_employee(*args, **kwargs):

        if current_user.user_role==UserRole.CUSTOMER:
            print(current_user.user_role)
            return redirect("/")
        return f(*args, **kwargs)
    return auth_employee
