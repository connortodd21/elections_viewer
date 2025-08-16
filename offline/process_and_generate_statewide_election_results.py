from common.input_helpers import getStateInput, getWriteIntermediateResultsInput
from data_processors.state_to_data_processor import STATES_TO_DATA_PROCESSOR

state = getStateInput()
writeIntermediateResults = getWriteIntermediateResultsInput()

data_processor = STATES_TO_DATA_PROCESSOR[state]()

# get raw data
data = data_processor.getRawData()
# cleanup data
data = data_processor.cleanData(data)
# filter unused rows
data = data_processor.filterData(data)
# drop unused columns
data = data_processor.dropData(data)
# write intermediate results if desired
if writeIntermediateResults:
    data_processor.setIntermediateData(data)
    data_processor.writeIntermediateDataset()
# generate county by county results
data = data_processor.generateCountyByCountyResults(data).sort_values([data_processor.YEAR, data_processor.ELECTION])
# save data to db
data_processor.writeDataToResults(data)