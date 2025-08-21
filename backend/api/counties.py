from backend.api import bp

@bp.route('/get_counties_by_state/<string:state>', methods=['GET'])
def get_counties_by_state(state):
    print(state)
    pass