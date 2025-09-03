from flask import Response

from app.api import bp
from app.errors.error_handler import error_response
from dataloader.counties_dataloader import get_county
from dataloader.election_results_dataloader import get_election_results_for_county as dataloader_get_election_results_for_county
from dataloader.election_results_dataloader import get_election_results_for_county_and_year as dataloader_get_election_results_for_county_and_year
from exceptions.InputException import *
from exceptions.DataNotGeneratedException import *
from formatters.json_formatter import dfToJson
from helpers.constants import *
from helpers.counties_helper import capitalizeCountyName

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

        # format (make all names capitalized)
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
        if not isinstance(county_name, str) or not isinstance(fips, str):
            raise InvalidInputError("Input must be a string")

        county_name = capitalizeCountyName(county_name)

        # get the state the county belongs to
        county_df = get_county(county_name, fips)
        state = county_df[STATE].iloc[0]
        county = county_df[NAME].iloc[0]

        # read elections data from db
        election_results = dataloader_get_election_results_for_county_and_year(county, state, year)

        # format (make all names capitalized)
        json_data = dfToJson(election_results)

        return Response(json_data, mimetype='application/json')
    except DataNotGeneratedException as e:
        return error_response(500, e.message)
    except InvalidInputError as e:
        return error_response(400, e.message)