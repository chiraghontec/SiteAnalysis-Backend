import json
import os
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.data_analyzer import DataAnalyzer
from unittest.mock import patch, mock_open

@pytest.fixture
def sample_thematic_data():
    """Sample thematic statistics data"""
    return {
        "elevation": 920,
        "landuse": "urban",
        "population_density": 12000,
        "rainfall_annual": 800,
        "soil_type": "clay loam"
    }

@pytest.fixture
def sample_route_data():
    """Sample routing data"""
    return {
        "distance": 1234.5,
        "duration": 3600,
        "segments": 5,
        "path": [
            {"lat": 12.97, "lng": 77.59},
            {"lat": 13.01, "lng": 77.62}
        ]
    }

@pytest.fixture
def sample_geoid_data():
    """Sample geoid data"""
    return {
        "geoid_height": 45.6,
        "undulation": 12.3,
        "reference_ellipsoid": "WGS84",
        "accuracy": "high"
    }

class TestDataAnalyzer:
    """Test suite for DataAnalyzer"""
    
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_data_files_thematic(self, mock_file, mock_listdir, sample_thematic_data):
        """Test loading thematic data files"""
        # Setup mocks
        mock_listdir.return_value = ['thematic_stats_12.9716_77.5946_20250814_120000.json']
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(sample_thematic_data)
        
        # Create analyzer
        analyzer = DataAnalyzer()
        
        # Call the method
        data_list = analyzer.load_data_files('thematic_stats')
        
        # Assertions
        assert len(data_list) == 1
        assert 'metadata' in data_list[0]
        assert 'data' in data_list[0]
        assert data_list[0]['data'] == sample_thematic_data
        assert data_list[0]['metadata']['lat'] == '12.9716'
        assert data_list[0]['metadata']['lng'] == '77.5946'
    
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_data_files_route(self, mock_file, mock_listdir, sample_route_data):
        """Test loading route data files"""
        # Setup mocks
        mock_listdir.return_value = ['route_12.9716_77.5946_to_28.6139_77.2090_20250814_120000.json']
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(sample_route_data)
        
        # Create analyzer
        analyzer = DataAnalyzer()
        
        # Call the method
        data_list = analyzer.load_data_files('route')
        
        # Assertions
        assert len(data_list) == 1
        assert 'metadata' in data_list[0]
        assert 'data' in data_list[0]
        assert data_list[0]['data'] == sample_route_data
        assert data_list[0]['metadata']['origin_lat'] == '12.9716'
        assert data_list[0]['metadata']['origin_lng'] == '77.5946'
        assert data_list[0]['metadata']['dest_lat'] == '28.6139'
        assert data_list[0]['metadata']['dest_lng'] == '77.2090'
    
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_api_summary(self, mock_file, mock_listdir, sample_thematic_data):
        """Test generating API summary"""
        # Setup mocks
        mock_listdir.return_value = ['thematic_stats_12.9716_77.5946_20250814_120000.json']
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(sample_thematic_data)
        
        # Create analyzer
        analyzer = DataAnalyzer()
        
        # Call the method
        summary = analyzer.generate_api_summary('thematic_stats')
        
        # Assertions
        assert 'api_type' in summary
        assert summary['api_type'] == 'thematic_stats'
        assert 'file_count' in summary
        assert summary['file_count'] == 1
        assert 'timestamp' in summary
        assert 'data_fields' in summary
        assert set(summary['data_fields']) == set(sample_thematic_data.keys())
