from common.defs import *
from common.input_helpers import getWriteIntermediateResultsInput
from data_processors.data_processor_factory import DEMOGRAPHICS_DATA_PROCESSOR

writeIntermediateResults = getWriteIntermediateResultsInput()

data_processor = DEMOGRAPHICS_DATA_PROCESSOR[POPULATION_TRENDS_BY_COUNTY]()

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
data = data_processor.processData(data)
# save data to db
data_processor.writeDataToResults(data)