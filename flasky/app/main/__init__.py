from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


# Permissions may also need to be checked from templates, so the Permission
# class with all the bit constants needs to be accessible to them.
# To avoid having to add a template argument in every render_template() call,
# a context processor can be used. Context processors make variables globally
# available to all templates.
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)