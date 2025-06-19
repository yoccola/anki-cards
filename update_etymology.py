#!/usr/bin/env python3
import csv
import sys

def load_etymology_data(csv_file):
    """語源データCSVファイルを読み込む"""
    etymology_data = {}
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word'].strip()
                etymology_data[word] = {
                    'etymology': row['etymology'],
                    'memory_aid': row['memory_aid'],
                    'synonyms': row['synonyms']
                }
    except FileNotFoundError:
        print(f"Error: {csv_file} not found")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: CSV file missing required column: {e}")
        sys.exit(1)
    
    return etymology_data

def update_tsv(input_file, output_file, etymology_data):
    """TSVファイルを更新する"""
    updated_count = 0
    total_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
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
                        updated_lines.append(f"【語源】{etymology_data[word]['etymology']}")
                        
                        # 記憶補助を追加
                        updated_lines.append(f"【記憶補助】{etymology_data[word]['memory_aid']}")
                        
                        # 類義語を追加
                        updated_lines.append(f"【類義語】{etymology_data[word]['synonyms']}")
                        
                        row[3] = '\n'.join(updated_lines)
                        updated_count += 1
                
                writer.writerow(row)
    
    print(f"✅ Updated TSV file saved to: {output_file}")
    print(f"📊 Statistics:")
    print(f"   - Total words processed: {total_count}")
    print(f"   - Words updated with etymology: {updated_count}")
    print(f"   - Words without etymology data: {total_count - updated_count}")

def main():
    # ファイルパス
    etymology_csv = "/Users/hi/work/claude_codes/anki-cards/etymology_data.csv"
    input_tsv = "/Users/hi/work/claude_codes/anki-cards/toeic_vocabulary/english_words.tsv"
    output_tsv = "/Users/hi/work/claude_codes/anki-cards/toeic_vocabulary/english_words_updated.tsv"
    
    # 語源データを読み込む
    print("📖 Loading etymology data...")
    etymology_data = load_etymology_data(etymology_csv)
    print(f"   Loaded {len(etymology_data)} word entries")
    
    # TSVファイルを更新
    print("\n🔄 Updating TSV file...")
    update_tsv(input_tsv, output_tsv, etymology_data)
    
    print("\n✨ Process completed successfully!")
    print(f"\n💡 To add more words:")
    print(f"   1. Edit {etymology_csv}")
    print(f"   2. Run this script again")

if __name__ == "__main__":
    main()