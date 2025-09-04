from flask import Response

from app.api import bp
from app.errors.error_handler import error_response
from dataloader.election_results_dataloader import get_election_results_for_state as dataloader_get_election_results_for_state
from dataloader.election_results_dataloader import get_election_results_for_state_and_year as dataloader_get_election_results_for_state_and_year
from exceptions.DataNotGeneratedException import *
from exceptions.InputException import *
from formatters.json_formatter import dfToJson
from formatters.state_results_formatter import format_results_for_state
from helpers.constants import *
from validators.state_validator import isValidState

@bp.route('/get_election_results_for_state/<string:state>', methods=['GET'])
def get_election_results_for_state(state: str) -> Response:
    """
    Given a state, get all the historical election data
    """
    try:
        # input validation 
        if not isinstance(state, str):
            raise InvalidInputError("Input must be a string")

        # input validation (ensure state is 2 letters and valid)
        if not isValidState(state):
            raise InvalidInputError("Please input a valid state")

        # read elections data from db
        election_results = dataloader_get_election_results_for_state(state)

        # format (convert county results to state results by year)
        state_results = format_results_for_state(election_results, state)
        json_data = dfToJson(state_results)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)

@bp.route('/get_election_results_for_state_and_year/<string:state>/<string:year>', methods=['GET'])
def get_election_results_for_state_and_year(state: str, year: str) -> Response:
    """
    Given a state and year, get the election data for that states and year
    """
    try:
        # input validation 
        if not isinstance(state, str) or not isinstance(year, str):
            raise InvalidInputError("Input must be a string")

        # input validation (ensure state is 2 letters and valid)
        if not isValidState(state):
            raise InvalidInputError("Please input a valid state")

        # read elections data from db
        election_results = dataloader_get_election_results_for_state_and_year(state, year)

        # format (make all names capitalized)
        state_results = format_results_for_state(election_results, state)
        json_data = dfToJson(state_results)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)