# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Anki Cards Etymology Enhancer - a Python tool that enriches TOEIC vocabulary flashcards with etymology, memory aids, and synonyms. The main script processes TSV files exported from Anki and updates them with additional learning information from a CSV database.

## Common Development Commands

```bash
# Install dependencies
make install
# or
pip install -r requirements.txt

# Run the main script
make run
# or
python update_etymology.py

# Run tests
make test

# Code quality checks
make lint      # Run flake8
make format    # Format with black
make mypy      # Type checking
make check-all # Run all checks

# Enhanced CLI version
python update_etymology_cli.py --help
```

## Architecture

The codebase has a simple architecture:

1. **Data Flow**:
   - Input: TSV file from Anki export + CSV etymology database
   - Processing: Matches words and adds etymology/memory_aid/synonyms columns
   - Output: Updated TSV files (UTF-8 and Shift-JIS versions)

2. **Key Files**:
   - `update_etymology.py` - Original script (maintains backward compatibility)
   - `update_etymology_cli.py` - Enhanced CLI version with progress bars and better error handling
   - `etymology_data.csv` - Source database for etymology information
   - `config.py` - Configuration management (when using enhanced version)

3. **Data Format**:
   - Etymology CSV: word, etymology, memory_aid, synonyms columns
   - Anki TSV: Variable columns, script adds Etymology, Memory Aid, and Synonyms fields

## Development Notes

- The project supports both UTF-8 and Shift-JIS encoding for Japanese compatibility
- Original script (`update_etymology.py`) uses hardcoded paths in `toeic_vocabulary/` directory
- Enhanced CLI version accepts custom input/output paths via command line arguments
- Type hints are used throughout the enhanced versions for better IDE support
- Tests use pytest and are located in the `tests/` directory