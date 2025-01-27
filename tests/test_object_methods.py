import pytest
from dataclasses import dataclass
from py_agent import PyAgent

@dataclass
class DataProcessor:
    """A utility class for processing and filtering data collections.
    
    This class provides methods for basic data processing operations such as
    sorting, removing duplicates, and filtering based on thresholds.
    
    Example:
        >>> processor = DataProcessor()
        >>> processor.process_list([3, 1, 2, 1, 3])
        [1, 2, 3]
        >>> processor.filter_numbers([1, 5, 3, 8, 2], 4)
        [5, 8]
    """
    def process_list(self, data: list) -> list:
        """Sort a list and remove duplicates"""
        return sorted(set(data))
    
    def filter_numbers(self, data: list, threshold: int) -> list:
        """Filter numbers greater than threshold"""
        return [x for x in data if x > threshold]
    
@pytest.fixture
def processor():
    return DataProcessor()

@pytest.fixture
def numbers():
    return [3, 1, 4, 1, 5, 9, 2, 6, 5]

@pytest.fixture
def variables(processor, numbers):
    return {
        'processor': processor,
        'numbers': numbers,
        'processed_data': None,
        'filtered_data': None
    }

@pytest.fixture
def variables_metadata():
    return {
        'processor': {
            'description': 'Data processing tool with various methods',
            'example': 'result = processor.process_list(numbers)'
        },
        'numbers': {
            'description': 'Input list of numbers',
            'example': 'filtered = processor.filter_numbers(numbers, 5)'
        },
        'processed_data': {
            'description': 'Store processed data here'
        },
        'filtered_data': {
            'description': 'Store filtered data here'
        }
    }

@pytest.fixture
def object_agent(llm_engine, variables, variables_metadata):
    return PyAgent(
        llm_engine,
        variables=variables,
        variables_metadata=variables_metadata
    )

def test_process_and_deduplicate(object_agent):
    object_agent.run("Use processor to sort and deduplicate numbers")
    processed_data = object_agent.get_object_from_runtime('processed_data')
    assert processed_data == [1, 2, 3, 4, 5, 6, 9]

def test_filter_numbers(object_agent):
    object_agent.run("Filter numbers greater than 4")
    filtered_data = object_agent.get_object_from_runtime('filtered_data')
    assert filtered_data == [5, 9, 6, 5] 