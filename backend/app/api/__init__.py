from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import counties
from app.api import election_results
from app.api import states
from app.api import population
from app.api import demographics