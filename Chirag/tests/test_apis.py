import pytest
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.thematic_statistics import ThematicStatisticsAPI
from src.api.routing import RoutingAPI
from src.api.geoid import GeoidAPI
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_response():
    """Create a mock response object"""
    mock = MagicMock()
    mock.json.return_value = {"status": "success", "data": {}}
    mock.raise_for_status.return_value = None
    return mock

@pytest.fixture
def sample_coordinates():
    """Sample test coordinates"""
    return {"lat": 12.9716, "lng": 77.5946}

@pytest.fixture
def sample_destination_coordinates():
    """Sample test destination coordinates"""
    return {"lat": 28.6139, "lng": 77.2090}

class TestThematicStatisticsAPI:
    """Test suite for ThematicStatisticsAPI"""
    
    @patch('requests.get')
    def test_get_statistics(self, mock_get, mock_response, sample_coordinates):
        """Test getting statistics for coordinates"""
        # Setup mock
        mock_get.return_value = mock_response
        
        # Create API client
        api = ThematicStatisticsAPI()
        
        # Call the method
        result = api.get_statistics(sample_coordinates)
        
        # Assertions
        assert 'timestamp' in result
        assert 'coordinates' in result
        assert result['coordinates'] == sample_coordinates
        assert 'parameters_used' in result
        assert 'statistics' in result
        
        # Verify API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert f"{api.base_url}/statistics" == args[0]
        assert 'params' in kwargs
        assert kwargs['params']['lat'] == sample_coordinates['lat']
        assert kwargs['params']['lng'] == sample_coordinates['lng']

class TestRoutingAPI:
    """Test suite for RoutingAPI"""
    
    @patch('requests.get')
    def test_get_route(self, mock_get, mock_response, sample_coordinates, sample_destination_coordinates):
        """Test getting route between coordinates"""
        # Setup mock
        mock_get.return_value = mock_response
        
        # Create API client
        api = RoutingAPI()
        
        # Call the method
        result = api.get_route(sample_coordinates, sample_destination_coordinates)
        
        # Assertions
        assert 'timestamp' in result
        assert 'origin' in result
        assert result['origin'] == sample_coordinates
        assert 'destination' in result
        assert result['destination'] == sample_destination_coordinates
        assert 'parameters_used' in result
        assert 'route' in result
        
        # Verify API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert f"{api.base_url}/route" == args[0]
        assert 'params' in kwargs
        assert kwargs['params']['origin_lat'] == sample_coordinates['lat']
        assert kwargs['params']['origin_lng'] == sample_coordinates['lng']
        assert kwargs['params']['dest_lat'] == sample_destination_coordinates['lat']
        assert kwargs['params']['dest_lng'] == sample_destination_coordinates['lng']

class TestGeoidAPI:
    """Test suite for GeoidAPI"""
    
    @patch('requests.get')
    def test_get_geoid_data(self, mock_get, mock_response, sample_coordinates):
        """Test getting geoid data for coordinates"""
        # Setup mock
        mock_get.return_value = mock_response
        
        # Create API client
        api = GeoidAPI()
        
        # Call the method
        result = api.get_geoid_data(sample_coordinates)
        
        # Assertions
        assert 'timestamp' in result
        assert 'coordinates' in result
        assert result['coordinates'] == sample_coordinates
        assert 'parameters_used' in result
        assert 'geoid_data' in result
        
        # Verify API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert f"{api.base_url}/data" == args[0]
        assert 'params' in kwargs
        assert kwargs['params']['lat'] == sample_coordinates['lat']
        assert kwargs['params']['lng'] == sample_coordinates['lng']
