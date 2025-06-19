#!/usr/bin/env python3
"""
Anki Cards Etymology Enhancer

A tool to enhance TOEIC vocabulary Anki cards with etymology information,
memory aids, and synonyms.
"""
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import click
from tqdm import tqdm


class EtymologyData:
    """Manages etymology data loading and access."""
    
    def __init__(self, csv_path: Path):
        self.data: Dict[str, Dict[str, str]] = {}
        self.csv_path = csv_path
        
    def load(self) -> None:
        """Load etymology data from CSV file."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Etymology data file not found: {self.csv_path}")
            
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word'].strip()
                self.data[word] = {
                    'etymology': row['etymology'],
                    'memory_aid': row['memory_aid'],
                    'synonyms': row['synonyms']
                }
                
    def get(self, word: str) -> Optional[Dict[str, str]]:
        """Get etymology data for a word."""
        return self.data.get(word)
    
    @property
    def word_count(self) -> int:
        """Get the number of words in the database."""
        return len(self.data)


class AnkiCardProcessor:
    """Processes Anki TSV files to add etymology information."""
    
    def __init__(self, etymology_data: EtymologyData):
        self.etymology_data = etymology_data
        self.stats = {
            'total': 0,
            'updated': 0,
            'skipped': 0
        }
        
    def process_file(self, input_path: Path, output_path: Path, 
                     encoding: str = 'utf-8') -> Dict[str, int]:
        """Process a TSV file and add etymology information."""
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        # Count total lines first for progress bar
        with open(input_path, 'r', encoding=encoding) as f:
            total_lines = sum(1 for _ in f)
            
        with open(input_path, 'r', encoding=encoding) as infile:
            with open(output_path, 'w', encoding=encoding, newline='') as outfile:
                reader = csv.reader(infile, delimiter='\t')
                writer = csv.writer(outfile, delimiter='\t')
                
                with tqdm(total=total_lines, desc="Processing cards") as pbar:
                    for row in reader:
                        pbar.update(1)
                        
                        if len(row) >= 4:
                            word = row[1].strip()
                            self.stats['total'] += 1
                            
                            # Check if word has etymology data
                            word_data = self.etymology_data.get(word)
                            if word_data:
                                self._update_row(row, word_data)
                                self.stats['updated'] += 1
                            else:
                                self.stats['skipped'] += 1
                        
                        writer.writerow(row)
                        
        return self.stats
    
    def _update_row(self, row: List[str], word_data: Dict[str, str]) -> None:
        """Update a row with etymology information."""
        meaning_field = row[3]
        lines = meaning_field.split('\n')
        
        # Keep the first line (Japanese translation)
        updated_lines = [lines[0] if lines else ""]
        
        # Add etymology information
        updated_lines.append(f"【語源】{word_data['etymology']}")
        updated_lines.append(f"【記憶補助】{word_data['memory_aid']}")
        updated_lines.append(f"【類義語】{word_data['synonyms']}")
        
        row[3] = '\n'.join(updated_lines)


def create_backup(file_path: Path) -> Path:
    """Create a backup of the file."""
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
    if file_path.exists():
        import shutil
        shutil.copy2(file_path, backup_path)
    return backup_path


@click.command()
@click.option(
    '--etymology-csv',
    type=click.Path(exists=True, path_type=Path),
    default='etymology_data.csv',
    help='Path to the etymology CSV file'
)
@click.option(
    '--input-tsv',
    type=click.Path(exists=True, path_type=Path),
    default='toeic_vocabulary/english_words.tsv',
    help='Path to the input TSV file'
)
@click.option(
    '--output-tsv',
    type=click.Path(path_type=Path),
    default='toeic_vocabulary/english_words_updated.tsv',
    help='Path to the output TSV file'
)
@click.option(
    '--encoding',
    type=str,
    default='utf-8',
    help='File encoding (default: utf-8)'
)
@click.option(
    '--backup/--no-backup',
    default=True,
    help='Create backup of output file if it exists'
)
def main(etymology_csv: Path, input_tsv: Path, output_tsv: Path, 
         encoding: str, backup: bool) -> None:
    """
    Enhance Anki cards with etymology information.
    
    This tool reads an Anki TSV export file and adds etymology,
    memory aids, and synonyms to each word from a CSV database.
    """
    click.echo("📚 Anki Cards Etymology Enhancer")
    click.echo("=" * 40)
    
    # Load etymology data
    click.echo("\n📖 Loading etymology data...")
    etymology = EtymologyData(etymology_csv)
    try:
        etymology.load()
        click.echo(f"   ✓ Loaded {etymology.word_count} word entries")
    except Exception as e:
        click.echo(f"   ✗ Error loading etymology data: {e}", err=True)
        sys.exit(1)
    
    # Create backup if requested
    if backup and output_tsv.exists():
        backup_path = create_backup(output_tsv)
        click.echo(f"\n💾 Created backup: {backup_path}")
    
    # Process the file
    click.echo(f"\n🔄 Processing TSV file...")
    processor = AnkiCardProcessor(etymology)
    
    try:
        stats = processor.process_file(input_tsv, output_tsv, encoding)
        
        click.echo(f"\n✅ Success! Output saved to: {output_tsv}")
        click.echo("\n📊 Statistics:")
        click.echo(f"   • Total cards processed: {stats['total']}")
        click.echo(f"   • Cards enhanced: {stats['updated']}")
        click.echo(f"   • Cards skipped (no data): {stats['skipped']}")
        
        if stats['skipped'] > 0:
            click.echo(f"\n💡 Tip: Add more words to {etymology_csv} to enhance more cards!")
            
    except Exception as e:
        click.echo(f"\n✗ Error processing file: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()