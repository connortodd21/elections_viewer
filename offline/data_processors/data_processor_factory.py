from common.defs import *
from data_processors.impl.demographic.DemographicTrendsByCounty import DemographicTrendsByCounty
from data_processors.impl.demographic.PopulationTrendsByCounty import PopulationTrendsByCountyDataProcessor
from data_processors.impl.state.CA import CAStateWideElectionDataProcessor
from data_processors.impl.state.MI import MIStateWideElectionDataProcessor

"""
Contains a mapping of all states (using 2-letter abbreviation) to their associated data processor class
"""
STATES_TO_DATA_PROCESSOR = {
    MI: MIStateWideElectionDataProcessor,
    CA: CAStateWideElectionDataProcessor
}

DEMOGRAPHICS_DATA_PROCESSOR = {
    POPULATION_TRENDS_BY_COUNTY: PopulationTrendsByCountyDataProcessor,
    DEMOGRAPHIC_TRENDS_BY_COUNTY: DemographicTrendsByCounty
}