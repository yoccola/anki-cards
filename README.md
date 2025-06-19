# Anki Cards Etymology Enhancer

TOEIC語彙のAnkiカードに語源情報、記憶補助、同義語を追加するPythonツールです。

## 概要

このプロジェクトは、Ankiからエクスポートした英単語カードに以下の情報を自動的に追加します：
- 語源（単語の成り立ちや語根）
- 記憶補助（覚えやすくするためのヒント）
- 同義語

## ファイル構成

```
anki-cards/
├── README.md               # このファイル
├── update_etymology.py     # メインスクリプト
├── etymology_data.csv      # 語源データベース
└── toeic_vocabulary/       # TOEIC語彙データ
    ├── english_words.tsv              # Ankiからエクスポートした元ファイル
    ├── english_words_updated.tsv      # 更新されたファイル（UTF-8）
    └── english_words_updated_shiftjis.tsv  # 更新されたファイル（Shift-JIS）
```

## 使用方法

1. **Ankiからデータをエクスポート**
   - Ankiでデッキを選択
   - ファイル → エクスポート
   - TSV形式で保存

2. **語源情報を追加**
   ```bash
   python update_etymology.py
   ```

3. **Ankiに再インポート**
   - Ankiを開く
   - ファイル → インポート
   - 更新されたTSVファイルを選択
   - フィールドマッピングを確認してインポート

## データ形式

### etymology_data.csv
語源データベースのCSVファイル形式：

| word | etymology | memory_aid | synonyms |
|------|-----------|------------|----------|
| conference | con-（共に）+ fer（運ぶ）+ -ence | 意見を「共に運ぶ」→会議 | meeting, convention |
| consider | con-（共に）+ sider（星） | 星を「共に見て」考える | think about, contemplate |

### TSVファイル
Ankiカードのフィールド：
- **Front**: 英単語
- **Back**: 日本語訳、品詞、例文など
- **Etymology**: 語源（新規追加）
- **Memory Aid**: 記憶補助（新規追加）
- **Synonyms**: 同義語（新規追加）

## 必要な環境

- Python 3.x
- pandas

インストール：
```bash
pip install pandas
```

## 語源データの追加方法

`etymology_data.csv`に新しい単語の語源情報を追加できます：

1. CSVファイルを開く
2. 新しい行に以下の情報を追加：
   - word: 英単語
   - etymology: 語源の説明
   - memory_aid: 覚え方のヒント
   - synonyms: 同義語（カンマ区切り）
3. ファイルを保存
4. `update_etymology.py`を再実行

## 注意事項

- 語源情報がない単語は元のまま保持されます
- 文字エンコーディングの問題を避けるため、UTF-8とShift-JIS両方のファイルが生成されます
- 更新前のデータは上書きされないため、元のファイルは保持されます