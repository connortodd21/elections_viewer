import json

from flask import Response

from app.api import bp
from app.errors.error_handler import error_response
from dataloader.counties_dataloader import get_county_by_fips
from dataloader.populations_dataloader import get_population_trend_for_county
from dataloader.populations_dataloader import get_population_trend_for_counties_in_state
from exceptions.DataNotGeneratedException import *
from exceptions.InputException import *
from formatters.json_formatter import dfToJson
from formatters.population_formatter import format_county_results_into_state
from helpers.constants import *
from validators.state_validator import isValidState


@bp.route('/get_population_trends_for_county/<string:fips>', methods=['GET'])
def get_population_trends_for_county(fips: str) -> Response:
    """
    Given a county fips, get the historical population data for that county
    """
    try:
        # input validation 
        if not isinstance(fips, str):
            raise InvalidInputError("Input must be a string")

        # get the county name
        county_df = get_county_by_fips(fips)
        county = county_df[NAME].iloc[0]

        # read population data from db
        population_trends = get_population_trend_for_county(fips, county)

        # format 
        json_data = dfToJson(population_trends)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)

@bp.route('/get_population_trends_for_state/<string:state>', methods=['GET'])
def get_population_trends_for_state(state: str) -> Response:
    """
    Given a county fips, get the historical population data for that county
    """
    try:
        # input validation 
        if not isinstance(state, str):
            raise InvalidInputError("Input must be a string")

        # input validation (ensure state is 2 letters and valid)
        if not isValidState(state):
            raise InvalidInputError("Please input a valid state")

        # read population data from db
        population_trends_for_county = get_population_trend_for_counties_in_state(state, STATE_TO_FIPS[state])

        # sum county-level data into state
        state_population_trends = format_county_results_into_state(population_trends_for_county)

        # format 
        json_data = dfToJson(state_population_trends)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)
