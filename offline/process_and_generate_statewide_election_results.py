from common.input_helpers import getStateInput, getWriteIntermediateResultsInput
from data_processors.data_processor_factory import STATES_TO_DATA_PROCESSOR

state = getStateInput()
writeIntermediateResults = getWriteIntermediateResultsInput()

data_processor = STATES_TO_DATA_PROCESSOR[state]()

# get raw data
data = data_processor.getRawData()
# filter unused rows
data = data_processor.filterData(data)
# cleanup data
data = data_processor.cleanData(data)
# drop unused columns
data = data_processor.dropData(data)
# write intermediate results if desired
if writeIntermediateResults:
    data_processor.setIntermediateData(data)
    data_processor.writeIntermediateDataset()
# generate county by county results
data = data_processor.processData(data).sort_values([data_processor.YEAR, data_processor.ELECTION])
# save data to db
data_processor.writeDataToResults(data)