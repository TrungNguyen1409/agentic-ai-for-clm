# Data Directory

This directory contains contract datasets for training, testing, and evaluation.

## Directory Structure

```
data/
├── raw/              # Original contract files (PDF, DOCX, etc.)
├── processed/        # Processed and cleaned contract text
├── synthetic/        # Synthetically generated contracts for testing
└── cuad/            # CUAD (Contract Understanding Atticus Dataset)
```

## Datasets

### CUAD Dataset

The Contract Understanding Atticus Dataset (CUAD) is a corpus of 510 contracts with over 13,000 expert annotations.

**Download:** https://github.com/TheAtticusProject/cuad

**Citation:**
```
@article{hendrycks2021cuad,
  title={CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review},
  author={Hendrycks, Dan and Burns, Collin and Chen, Anya and Ball, Spencer},
  journal={arXiv preprint arXiv:2103.06268},
  year={2021}
}
```

### Synthetic Data

For initial testing and development, synthetic contracts can be generated using LLMs.

### Data Privacy

**IMPORTANT:** Never commit actual contracts or sensitive data to version control.

- All data directories are gitignored
- Use synthetic or publicly available datasets for development
- Anonymize any real contracts before processing
- Follow data retention policies

## Data Formats

### Raw Contracts
- **Formats:** PDF, DOCX, DOC, TXT
- **Location:** `data/raw/`
- **Naming:** Use descriptive names (e.g., `services_agreement_2024_01.pdf`)

### Processed Contracts
- **Format:** JSON
- **Location:** `data/processed/`
- **Schema:**
  ```json
  {
    "contract_id": "unique-id",
    "title": "Contract title",
    "content": "Full contract text",
    "metadata": {
      "contract_type": "services_agreement",
      "parties": ["Party A", "Party B"],
      "date": "2024-01-01",
      "jurisdiction": "California"
    },
    "clauses": [
      {
        "clause_id": "1.1",
        "clause_type": "services",
        "text": "Clause text here"
      }
    ]
  }
  ```

## Usage

### Loading Contracts

```python
from pathlib import Path
import json

# Load processed contract
def load_contract(contract_id: str):
    contract_path = Path(f"data/processed/{contract_id}.json")
    with open(contract_path, 'r') as f:
        return json.load(f)

# Load raw contract
from pypdf import PdfReader

def load_pdf_contract(filename: str):
    pdf_path = Path(f"data/raw/{filename}")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
```

### Processing Pipeline

1. Place raw contracts in `data/raw/`
2. Run processing pipeline: `python src/pipeline/process_contracts.py`
3. Processed contracts appear in `data/processed/`

## Data Quality Guidelines

### Inclusion Criteria
- Contracts must be in English (or configured language)
- Minimum length: 500 words
- Must be machine-readable (no scanned images without OCR)
- Should represent real-world contract structures

### Exclusion Criteria
- Contracts with excessive redactions
- Poor OCR quality (< 80% confidence)
- Duplicate contracts
- Contracts with sensitive/confidential information

## Annotation Guidelines

For evaluation datasets, annotations should include:

1. **Risk Labels**: High/Medium/Low risk clauses
2. **Clause Types**: Payment, liability, termination, etc.
3. **Obligations**: Extracted obligations with parties and deadlines
4. **Dependencies**: Relationships between clauses

See `docs/guides/annotation_guide.md` for detailed instructions.

## Statistics

Track dataset statistics in this section:

- Total contracts: TBD
- Contract types: TBD
- Average length: TBD
- Date range: TBD

## Contributing Data

If you have contracts to contribute:

1. Ensure you have rights to share the contract
2. Anonymize all party names and sensitive information
3. Convert to standard format
4. Submit via pull request with metadata
