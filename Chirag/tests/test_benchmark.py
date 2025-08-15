import pytest
import time
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.benchmark import benchmark_api_call, log_benchmark

def dummy_function(param1, param2=None):
    """Dummy function for testing benchmark_api_call"""
    time.sleep(0.1)  # Sleep to simulate work
    return {"param1": param1, "param2": param2}

class TestBenchmarkUtils:
    """Test suite for benchmark utilities"""
    
    def test_benchmark_api_call(self):
        """Test benchmarking an API call"""
        # Call the benchmark function
        result, execution_time = benchmark_api_call(dummy_function, "test", param2="value")
        
        # Assertions
        assert result == {"param1": "test", "param2": "value"}
        assert execution_time > 0  # Execution time should be positive
        assert execution_time >= 100  # Should be at least 100ms due to sleep
        
        # Check if the benchmark log file was created
        assert os.path.exists('data/benchmarks/api_benchmark.jsonl')
        
        # Check if the log entry is valid
        with open('data/benchmarks/api_benchmark.jsonl', 'r') as f:
            last_line = f.readlines()[-1]
            log_entry = json.loads(last_line)
            
            assert 'timestamp' in log_entry
            assert 'function' in log_entry
            assert log_entry['function'] == 'dummy_function'
            assert 'execution_time_ms' in log_entry
            assert log_entry['execution_time_ms'] > 0
    
    def test_log_benchmark(self):
        """Test logging benchmark results"""
        # Ensure directory exists
        os.makedirs('data/benchmarks', exist_ok=True)
        
        # Call the log function
        log_benchmark('test_function', ['arg1', 'arg2'], {'kwarg': 'value'}, 123.45)
        
        # Check if the log file was created
        assert os.path.exists('data/benchmarks/api_benchmark.jsonl')
        
        # Check if the log entry is valid
        with open('data/benchmarks/api_benchmark.jsonl', 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
            log_entry = json.loads(last_line)
            
            assert 'timestamp' in log_entry
            assert 'function' in log_entry
            assert log_entry['function'] == 'test_function'
            assert 'execution_time_ms' in log_entry
            assert log_entry['execution_time_ms'] == 123.45
            assert 'args' in log_entry
            assert 'kwargs' in log_entry
