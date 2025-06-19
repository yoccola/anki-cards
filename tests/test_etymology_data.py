"""Tests for EtymologyData class."""
import pytest
from pathlib import Path
import tempfile
import csv
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from update_etymology_cli import EtymologyData


class TestEtymologyData:
    """Test cases for EtymologyData class."""
    
    @pytest.fixture
    def sample_csv(self):
        """Create a temporary CSV file with sample data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'etymology', 'memory_aid', 'synonyms'])
            writer.writerow(['test', 'test etymology', 'test memory', 'test1, test2'])
            writer.writerow(['example', 'ex- (out) + ample', 'sample out', 'instance, case'])
            return Path(f.name)
    
    def test_load_valid_csv(self, sample_csv):
        """Test loading a valid CSV file."""
        etym = EtymologyData(sample_csv)
        etym.load()
        
        assert etym.word_count == 2
        assert 'test' in etym.data
        assert 'example' in etym.data
        
        # Clean up
        sample_csv.unlink()
    
    def test_get_existing_word(self, sample_csv):
        """Test getting data for an existing word."""
        etym = EtymologyData(sample_csv)
        etym.load()
        
        data = etym.get('test')
        assert data is not None
        assert data['etymology'] == 'test etymology'
        assert data['memory_aid'] == 'test memory'
        assert data['synonyms'] == 'test1, test2'
        
        # Clean up
        sample_csv.unlink()
    
    def test_get_nonexistent_word(self, sample_csv):
        """Test getting data for a non-existent word."""
        etym = EtymologyData(sample_csv)
        etym.load()
        
        data = etym.get('nonexistent')
        assert data is None
        
        # Clean up
        sample_csv.unlink()
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file."""
        etym = EtymologyData(Path('nonexistent.csv'))
        
        with pytest.raises(FileNotFoundError):
            etym.load()