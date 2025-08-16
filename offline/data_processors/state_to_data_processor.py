from common.defs import *
from data_processors.impl.MI import MIStateWideElectionDataProcessor
from data_processors.impl.CA import CAStateWideElectionDataProcessor

"""
Contains a mapping of all states (using 2-letter abbreviation) to their associated data processor class
"""
STATES_TO_DATA_PROCESSOR = {
    MI: MIStateWideElectionDataProcessor,
    CA: CAStateWideElectionDataProcessor
}