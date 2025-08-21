from flask import Response

from app.api import bp
from dataloader.counties_dataloader import get_counties_by_state as dataloader_get_counties_by_state
from formatters.json_formatter import dfToJson
from validators.state_validator import isValidState

@bp.route('/get_counties_by_state/<string:state>', methods=['GET'])
def get_counties_by_state(state):
    """
    Given a state, return a list of all US counties within the state 
    """

    # input validation (ensure state is 2 letters and valid)
    if not isValidState(state):
        error_message = "Please input a valid state"
        print(error_message)
        raise KeyError(error_message)
    # read from db
    counties = dataloader_get_counties_by_state(state)

    # format
    json_data = dfToJson(counties)

    return Response(json_data, mimetype='application/json')
    