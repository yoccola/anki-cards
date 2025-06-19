#!/usr/bin/env python3
"""
Improved version of update_etymology.py with type hints and better structure.
Maintains compatibility with the original while adding improvements.
"""
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse


def load_etymology_data(csv_file: str) -> Dict[str, Dict[str, str]]:
    """
    語源データCSVファイルを読み込む
    
    Args:
        csv_file: Path to the CSV file containing etymology data
        
    Returns:
        Dictionary mapping words to their etymology data
    """
    etymology_data: Dict[str, Dict[str, str]] = {}
    csv_path = Path(csv_file)
    
    if not csv_path.exists():
        print(f"Error: {csv_file} not found")
        sys.exit(1)
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word'].strip()
                etymology_data[word] = {
                    'etymology': row['etymology'],
                    'memory_aid': row['memory_aid'],
                    'synonyms': row['synonyms']
                }
    except KeyError as e:
        print(f"Error: CSV file missing required column: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    return etymology_data


def update_tsv(input_file: str, output_file: str, 
               etymology_data: Dict[str, Dict[str, str]]) -> None:
    """
    TSVファイルを更新する
    
    Args:
        input_file: Path to input TSV file
        output_file: Path to output TSV file
        etymology_data: Dictionary containing etymology information
    """
    updated_count = 0
    total_count = 0
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    if not input_path.exists():
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
                reader = csv.reader(infile, delimiter='\t')
                writer = csv.writer(outfile, delimiter='\t')
                
                for row in reader:
                    if len(row) >= 4:
                        word = row[1].strip()
                        total_count += 1
                        
                        # 英単語が語源データベースにある場合
                        if word in etymology_data:
                            meaning_field = row[3]
                            lines = meaning_field.split('\n')
                            
                            # 最初の行（日本語訳）を保持
                            updated_lines = [lines[0] if lines else ""]
                            
                            # 語源を追加
                            updated_lines.append(
                                f"【語源】{etymology_data[word]['etymology']}"
                            )
                            
                            # 記憶補助を追加
                            updated_lines.append(
                                f"【記憶補助】{etymology_data[word]['memory_aid']}"
                            )
                            
                            # 類義語を追加
                            updated_lines.append(
                                f"【類義語】{etymology_data[word]['synonyms']}"
                            )
                            
                            row[3] = '\n'.join(updated_lines)
                            updated_count += 1
                    
                    writer.writerow(row)
                    
    except Exception as e:
        print(f"Error processing TSV file: {e}")
        sys.exit(1)
    
    print(f"✅ Updated TSV file saved to: {output_file}")
    print(f"📊 Statistics:")
    print(f"   - Total words processed: {total_count}")
    print(f"   - Words updated with etymology: {updated_count}")
    print(f"   - Words without etymology data: {total_count - updated_count}")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Anki Cards Etymology Enhancer - Add etymology to your Anki cards"
    )
    
    # Use config.py for defaults if available
    try:
        from config import DEFAULT_ETYMOLOGY_CSV, DEFAULT_INPUT_TSV, DEFAULT_OUTPUT_TSV
        etymology_default = str(DEFAULT_ETYMOLOGY_CSV)
        input_default = str(DEFAULT_INPUT_TSV)
        output_default = str(DEFAULT_OUTPUT_TSV)
    except ImportError:
        # Fallback to hardcoded paths
        etymology_default = "/Users/hi/work/claude_codes/anki-cards/etymology_data.csv"
        input_default = "/Users/hi/work/claude_codes/anki-cards/toeic_vocabulary/english_words.tsv"
        output_default = "/Users/hi/work/claude_codes/anki-cards/toeic_vocabulary/english_words_updated.tsv"
    
    parser.add_argument(
        '--etymology-csv',
        type=str,
        default=etymology_default,
        help='Path to etymology CSV file'
    )
    parser.add_argument(
        '--input-tsv',
        type=str,
        default=input_default,
        help='Path to input TSV file'
    )
    parser.add_argument(
        '--output-tsv',
        type=str,
        default=output_default,
        help='Path to output TSV file'
    )
    
    return parser.parse_args()


def main() -> None:
    """Main function."""
    # Parse arguments
    args = parse_arguments()
    
    # 語源データを読み込む
    print("📖 Loading etymology data...")
    etymology_data = load_etymology_data(args.etymology_csv)
    print(f"   Loaded {len(etymology_data)} word entries")
    
    # TSVファイルを更新
    print("\n🔄 Updating TSV file...")
    update_tsv(args.input_tsv, args.output_tsv, etymology_data)
    
    print("\n✨ Process completed successfully!")
    print(f"\n💡 To add more words:")
    print(f"   1. Edit {args.etymology_csv}")
    print(f"   2. Run this script again")


if __name__ == "__main__":
    main()