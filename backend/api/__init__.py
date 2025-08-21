from flask import Blueprint

bp = Blueprint('api', __name__)

from backend.api import counties