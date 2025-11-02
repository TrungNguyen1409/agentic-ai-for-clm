# Setup Guide

This guide will help you set up the Multi-Agent CLM System for development and testing.

## Prerequisites

- Python 3.11 or higher
- Git
- AWS Account (for Textract)
- Supabase Account
- OpenAI API Key or Anthropic API Key
- LangFuse Account (optional, for observability)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agentic-ai-for-clm
```

### 2. Set Up Python Environment

Using venv:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Using Poetry (recommended):
```bash
# Install Poetry if you haven't
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
poetry shell
```

### 3. Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Using Poetry:
```bash
poetry install
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```bash
# LLM Provider
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview

# AWS (for Textract)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# LangFuse (optional)
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
```

### 5. Set Up Supabase Vector Database

1. Create a new Supabase project at https://supabase.com
2. Enable the pgvector extension:
   - Go to SQL Editor in Supabase dashboard
   - Run: `CREATE EXTENSION IF NOT EXISTS vector;`
3. Create the contracts table:

```sql
-- Create contracts table
CREATE TABLE contracts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT,
  content TEXT,
  embedding VECTOR(1536),
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX ON contracts USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create clauses table
CREATE TABLE clauses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_id UUID REFERENCES contracts(id),
  clause_text TEXT,
  clause_type TEXT,
  embedding VECTOR(1536),
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX ON clauses USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 6. Set Up AWS Textract

1. Create an AWS account at https://aws.amazon.com
2. Create an IAM user with Textract permissions:
   - Go to IAM Console
   - Create user with programmatic access
   - Attach policy: `AmazonTextractFullAccess`
   - Save the access key and secret key
3. Add credentials to `.env` file

### 7. Verify Installation

Run tests to verify everything is set up correctly:

```bash
pytest tests/ -v
```

Run a simple test:

```bash
python -c "from src.core.config import settings; print(f'Config loaded: {settings.llm_provider}')"
```

## Development Setup

### Code Quality Tools

The project uses several code quality tools:

- **Black**: Code formatting
- **Ruff**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

Run formatting:
```bash
black src/ tests/
```

Run linting:
```bash
ruff check src/ tests/
```

Run type checking:
```bash
mypy src/
```

### Pre-commit Hooks (Optional)

Set up pre-commit hooks to automatically format and lint:

```bash
pip install pre-commit
pre-commit install
```

## Running the System

### Basic Usage

```bash
# Run the main application
python src/main.py

# Or using Poetry
poetry run python src/main.py
```

### Interactive Development

Start Jupyter for interactive development:

```bash
jupyter notebook notebooks/
```

### Running Experiments

```bash
python experiments/run_evaluation.py --config configs/evaluation/baseline_comparison.yaml
```

## Data Setup

### CUAD Dataset

Download the CUAD (Contract Understanding Atticus Dataset):

```bash
# Create data directory
mkdir -p data/cuad

# Download CUAD dataset
cd data/cuad
wget https://github.com/TheAtticusProject/cuad/archive/refs/heads/main.zip
unzip main.zip
```

### Sample Contracts

Place your test contracts in:
- `data/raw/` - Original contract files (PDF, DOCX)
- `data/processed/` - Processed contract text

## Troubleshooting

### Issue: ImportError for pydantic or other packages

**Solution:** Ensure you've activated the virtual environment and installed all dependencies.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Supabase connection errors

**Solution:** Check your Supabase URL and keys in `.env`. Ensure the pgvector extension is enabled.

### Issue: AWS Textract authentication errors

**Solution:** Verify your AWS credentials and region in `.env`. Check IAM permissions for Textract.

### Issue: LangFuse tracing not working

**Solution:** LangFuse is optional. If you don't want to use it, set `LANGFUSE_PUBLIC_KEY=""` in `.env`.

## Next Steps

- Read the [Architecture Documentation](docs/architecture/README.md)
- Explore the [API Documentation](docs/api/README.md)
- Follow the [Development Guide](docs/guides/development.md)
- Check out the [Jupyter Notebooks](notebooks/)

## Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review existing issues in the repository
3. Contact the maintainer: Trung Nguyen
