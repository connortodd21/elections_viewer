from backend.app.api import bp

@bp.route('/get_counties_by_state/<string:state>', methods=['GET'])
def get_counties_by_state(state):
    """
    Given a state, return a list of all US counties within the state 
    """

    # input validation (ensure state is 2 letters and valid)

    # read from db

    # format

    # return
    print(state)
    pass