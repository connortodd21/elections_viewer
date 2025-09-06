import json

from flask import Response

from app.api import bp
from app.errors.error_handler import error_response
from dataloader.counties_dataloader import get_county
from dataloader.election_results_dataloader import get_election_results_for_county as dataloader_get_election_results_for_county
from dataloader.election_results_dataloader import get_election_results_for_county_and_year as dataloader_get_election_results_for_county_and_year
from dataloader.election_results_dataloader import get_election_results_for_state as dataloader_get_election_results_for_state
from exceptions.DataNotGeneratedException import *
from exceptions.InputException import *
from formatters.json_formatter import dfToJson
from formatters.swing_counties_formatter import get_swing_counties as formatter_get_swing_counties
from helpers.constants import *
from helpers.counties_helper import capitalizeCountyName
from helpers.states_helper import convert_state_to_abbreviation
from validators.state_validator import isValidState

@bp.route('/get_election_results_for_county/<string:fips>/<string:county_name>', methods=['GET'])
def get_election_results_for_county(county_name: str, fips: str) -> Response:
    """
    Given a county name and fips, get the historical election data for that county
    """
    try:
        # input validation 
        if not isinstance(county_name, str) or not isinstance(fips, str):
            raise InvalidInputError("Input must be a string")

        county_name = capitalizeCountyName(county_name)

        # get the state the county belongs to
        county_df = get_county(county_name, fips)
        state = county_df[STATE].iloc[0]
        county = county_df[NAME].iloc[0]

        # read elections data from db
        election_results = dataloader_get_election_results_for_county(county, state)

        # format 
        json_data = dfToJson(election_results)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)

@bp.route('/get_election_results_for_county_and_year/<string:fips>/<string:county_name>/<string:year>', methods=['GET'])
def get_election_results_for_county_and_year(county_name: str, fips: str, year: str) -> Response:
    """
    Given a county name and fips, get the election data for that county and year
    """
    try:
        # input validation 
        if not isinstance(county_name, str) or not isinstance(fips, str) or not isinstance(year, str):
            raise InvalidInputError("Input must be a string")

        county_name = capitalizeCountyName(county_name)

        # get the state the county belongs to
        county_df = get_county(county_name, fips)
        state = county_df[STATE].iloc[0]
        county = county_df[NAME].iloc[0]

        # read elections data from db
        election_results = dataloader_get_election_results_for_county_and_year(county, state, year)

        # format 
        json_data = dfToJson(election_results)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)

@bp.route('/get_swing_counties/<string:state>', methods=['GET'])
def get_swing_counties(state: str) -> Response:
    """
        Get all swing counties for a given state. Swing counties are defined as counties which have
        voted for different winning parties in different election years.

        For example:
            A county which voted Republican in 2016 and Democrat in 2024 is a swing county
            A county which voted Republican in 2016 and Democrat in 2018 is a swing county

        Any county which always votes for the same party is not a swing county
    """
    try:
        # input validation 
        if not isinstance(state, str):
            raise InvalidInputError("Input must be a string")

        state = convert_state_to_abbreviation(state)

        # input validation (ensure state is 2 letters and valid)
        if not isValidState(state):
            raise InvalidInputError("Please input a valid state")

        # read elections data from db
        election_results = dataloader_get_election_results_for_state(state)

        # format (filter for swing counties)
        swing_counties = formatter_get_swing_counties(election_results)
        json_data = json.dumps(swing_counties)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)