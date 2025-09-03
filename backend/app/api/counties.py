import json

from flask import Response

from app.api import bp
from app.errors.error_handler import error_response
from dataloader.counties_dataloader import get_counties_by_state as dataloader_get_counties_by_state
from dataloader.counties_dataloader import get_county
from dataloader.election_results_dataloader import get_statewide_election_years_for_county
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


@bp.route('/get_county_election_years/<string:fips>/<string:county_name>', methods=['GET'])
def get_county_statewide_election_years(county_name: str, fips: str) -> Response:
    """
    Given a county name and fips, get the years there was a statewide election
    """
    try:
        # input validation 
        if not isinstance(county_name, str) or not isinstance(fips, str):
            print(county_name, fips, type(fips))
            raise InvalidInputError("Inputs must be strings")

        county_name = capitalizeCountyName(county_name)

        # get the state the county belongs to
        county_df = get_county(county_name, fips)
        state = county_df[STATE].iloc[0]
        county = county_df[NAME].iloc[0]

        # read elections years from db
        election_years = get_statewide_election_years_for_county(county, state)

        # format (make json serializable)
        json_data = json.dumps(election_years.tolist())

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)