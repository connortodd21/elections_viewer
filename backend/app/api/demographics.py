from flask import Response

from app.api import bp
from app.errors.error_handler import error_response
from dataloader.counties_dataloader import get_county_by_fips
from dataloader.demographics_dataloader import get_demographic_trend_for_county
from dataloader.demographics_dataloader import get_demographic_trend_for_state
from exceptions.DataNotGeneratedException import *
from exceptions.InputException import *
from formatters.demographics_formatter import format_county_results_into_state
from formatters.json_formatter import dfToJson
from helpers.constants import *
from validators.state_validator import isValidState


@bp.route('/get_demographic_trends_for_county/<string:fips>', methods=['GET'])
def get_demographic_trends_for_county(fips: str) -> Response:
    """
    Given a county fips, get the historical demographic data for that county
    """
    try:
        # input validation 
        if not isinstance(fips, str):
            raise InvalidInputError("Input must be a string")

        # get the county name
        county_df = get_county_by_fips(fips)
        state = county_df[STATE].iloc[0]
        county = county_df[NAME].iloc[0]

        # read demographic data from db
        demographic_trends = get_demographic_trend_for_county(fips, county, state)

        # format 
        json_data = dfToJson(demographic_trends)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)

@bp.route('/get_demographic_trends_for_state/<string:state>', methods=['GET'])
def get_demographic_trends_for_state(state: str) -> Response:
    """
    Given a state, get the historical demographic data for that state
    """
    try:
        # input validation 
        if not isinstance(state, str):
            raise InvalidInputError("Input must be a string")

        # input validation (ensure state is 2 letters and valid)
        if not isValidState(state):
            raise InvalidInputError("Please input a valid state")

        # read demographic data from db
        demographic_trends = get_demographic_trend_for_state(state)

        # sum county-level data into state
        state_demographic_trends = format_county_results_into_state(demographic_trends)

        # format 
        json_data = dfToJson(state_demographic_trends)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)