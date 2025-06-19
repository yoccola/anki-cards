"""Tests for AnkiCardProcessor class."""
import pytest
from pathlib import Path
import tempfile
import csv
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from update_etymology_cli import EtymologyData, AnkiCardProcessor


class TestAnkiCardProcessor:
    """Test cases for AnkiCardProcessor class."""
    
    @pytest.fixture
    def etymology_data(self):
        """Create etymology data with test entries."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'etymology', 'memory_aid', 'synonyms'])
            writer.writerow(['anyway', 'any + way', 'any way to go', 'anyhow, regardless'])
            writer.writerow(['conference', 'con- + fer', 'bring together', 'meeting, convention'])
            csv_path = Path(f.name)
        
        etym = EtymologyData(csv_path)
        etym.load()
        csv_path.unlink()
        return etym
    
    @pytest.fixture
    def sample_tsv(self):
        """Create a temporary TSV file with sample Anki data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
            writer = csv.writer(f, delimiter='\t')
            # Anki format: deck, word, example, meaning, example_audio, word_audio, extra
            writer.writerow([
                'TOEIC Deck',
                'anyway',
                "(Let's try anyway.)",
                'とにかく',
                '[sound:01-01.mp3]',
                '[sound:01-02.mp3]',
                ''
            ])
            writer.writerow([
                'TOEIC Deck',
                'unknown',
                '(Unknown word)',
                '未知の単語',
                '[sound:02-01.mp3]',
                '[sound:02-02.mp3]',
                ''
            ])
            return Path(f.name)
    
    def test_process_file_with_matches(self, etymology_data, sample_tsv):
        """Test processing a file with matching words."""
        processor = AnkiCardProcessor(etymology_data)
        output_path = sample_tsv.with_suffix('.output.tsv')
        
        stats = processor.process_file(sample_tsv, output_path)
        
        assert stats['total'] == 2
        assert stats['updated'] == 1  # Only 'anyway' should be updated
        assert stats['skipped'] == 1  # 'unknown' should be skipped
        
        # Verify output content
        with open(output_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
            
            # Check first row (anyway - should be updated)
            assert '【語源】any + way' in rows[0][3]
            assert '【記憶補助】any way to go' in rows[0][3]
            assert '【類義語】anyhow, regardless' in rows[0][3]
            
            # Check second row (unknown - should not be updated)
            assert '【語源】' not in rows[1][3]
        
        # Clean up
        sample_tsv.unlink()
        output_path.unlink()
    
    def test_process_nonexistent_file(self, etymology_data):
        """Test processing a non-existent file."""
        processor = AnkiCardProcessor(etymology_data)
        
        with pytest.raises(FileNotFoundError):
            processor.process_file(
                Path('nonexistent.tsv'),
                Path('output.tsv')
            )
    
    def test_process_empty_file(self, etymology_data):
        """Test processing an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
            input_path = Path(f.name)
        
        output_path = input_path.with_suffix('.output.tsv')
        processor = AnkiCardProcessor(etymology_data)
        
        stats = processor.process_file(input_path, output_path)
        
        assert stats['total'] == 0
        assert stats['updated'] == 0
        assert stats['skipped'] == 0
        
        # Clean up
        input_path.unlink()
        output_path.unlink()