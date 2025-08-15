VALID_STATES = set([
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
])

def getStateInput() -> str:
    state = None
    attempts = 0
    while True:
        state = input("Which state are you generating data for (use two letter representation): ")
        if state in VALID_STATES:
            return state
        else:
            print("Please input a valid state")
        if attempts > 5:
            print("Too many failures, try running again")
            exit(1)
        attempts += 1