from flask import Response
from werkzeug.http import HTTP_STATUS_CODES

from app.api import bp
from app.errors.error_handler import error_response
from dataloader.counties_dataloader import get_counties_by_state as dataloader_get_counties_by_state
from dataloader.counties_dataloader import get_county
from dataloader.election_results_dataloader import get_election_results_for_county as dataloader_get_election_results_for_county
from exceptions.InputException import *
from exceptions.DataNotGeneratedException import *
from formatters.json_formatter import dfToJson
from helpers.constants import *
from helpers.counties_helper import capitalizeCountyName
from validators.state_validator import isValidState

@bp.route('/get_counties_by_state/<string:state>', methods=['GET'])
def get_counties_by_state(state: str) -> Response:
    """
    Given a state, return a list of all US counties within the state 
    """
    # input validation (ensure state is 2 letters and valid)
    if not isValidState(state):
        raise InvalidInputError("Please input a valid state")
    # read from db
    counties = dataloader_get_counties_by_state(state)

    # format
    json_data = dfToJson(counties)

    return Response(json_data, mimetype='application/json')


@bp.route('/get_election_results_for_county/<string:county_name>', methods=['GET'])
def get_election_results_for_county(county_name: str) -> Response:
    """
    Given a county name, get the historical election data for that county
    """
    try:
        # input validation 
        if not isinstance(county_name, str):
            raise InvalidInputError("Input must be a string")

        county_name = capitalizeCountyName(county_name)

        # get the state the county belongs to
        county_df = get_county(county_name)
        state = county_df[STATE].iloc[0]
        county = county_df[NAME].iloc[0]

        # read elections data from db
        election_results = dataloader_get_election_results_for_county(county, state)

        # format (make all names capitalized)
        json_data = dfToJson(election_results)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)