from common.defs import *

def getStateInput() -> str:
    state = None
    attempts = 0
    while True:
        state = input("Which state are you generating data for (use two letter representation): ")
        if state in VALID_US_STATES:
            return state
        else:
            print("Please input a valid state")
        if attempts > 5:
            print("Too many failures, try running again")
            exit(1)
        attempts += 1

def getWriteIntermediateResultsInput() -> bool:
    valid_answers = set(['y', 'n'])
    attempts = 0
    while True:
        ans = input("Do you want to write intermediate results? (y/n): ")
        if len(ans) == 1 and ans in valid_answers:
            return True if ans == 'y' else False
        else:
            print("\nPlease input a valid response (either 'y' or 'n')\n")
        if attempts > 5:
            print("Too many failures, try running again")
            exit(1)
        attempts += 1