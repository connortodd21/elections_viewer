from common.input_helpers import getStateInput, getWriteIntermediateResultsInput
from data_processors.state_to_data_processor import STATES_TO_DATA_PROCESSOR

state = getStateInput()
writeIntermediateResults = getWriteIntermediateResultsInput()

data_processor = STATES_TO_DATA_PROCESSOR[state]()

data = data_processor.getRawData()
data = data_processor.filterData(data)
data = data_processor.cleanData(data)
data = data_processor.dropData(data)
if writeIntermediateResults:
    data_processor.setIntermediateData(data)
    data_processor.writeIntermediateDataset()
data = data_processor.generateCountyByCountyResults(data).sort_values(["year", "election"])
data_processor.writeDataToResults(data)