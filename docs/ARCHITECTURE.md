# System Architecture

This document describes the architecture of the Multi-Agent CLM System.

## Overview

The system implements a modular multi-agent architecture where specialized agents collaborate to analyze contracts. The architecture follows these key principles:

1. **Modularity**: Each agent is independently configurable and replaceable
2. **Explainability**: All agent decisions include reasoning traces
3. **Scalability**: Agents can run concurrently or sequentially
4. **Observability**: Full tracing through LangFuse integration

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Interface                         │
│              (Web UI / API / Jupyter Notebook)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Orchestration Layer                         │
│                    (LangGraph)                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Agent Coordinator & State Management                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────┬──────────────┬──────────────┬──────────┬──────────┘
          │              │              │          │
    ┌─────▼─────┐  ┌────▼─────┐  ┌─────▼─────┐  ┌▼──────────┐
    │   Risk    │  │  Clause  │  │Obligation │  │Dependency │
    │ Analysis  │  │Alignment │  │ Tracking  │  │   Graph   │
    │   Agent   │  │  Agent   │  │   Agent   │  │   Agent   │
    └─────┬─────┘  └────┬─────┘  └─────┬─────┘  └┬──────────┘
          │              │              │          │
    ┌─────▼──────────────▼──────────────▼──────────▼─────────┐
    │              Shared Services Layer                      │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
    │  │ LLM Provider │  │Vector Store  │  │  Document    │  │
    │  │  (OpenAI/    │  │ (Supabase)   │  │ Processing   │  │
    │  │  Anthropic)  │  │              │  │ (Textract)   │  │
    │  └──────────────┘  └──────────────┘  └──────────────┘  │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
    │  │ Observability│  │   Config     │  │    Logger    │  │
    │  │  (LangFuse)  │  │   Manager    │  │              │  │
    │  └──────────────┘  └──────────────┘  └──────────────┘  │
    └─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Agent Layer

Each agent is specialized for a specific contract analysis task:

#### Risk Analysis Agent
- **Purpose**: Identify red-flag clauses, liability gaps, and unbalanced terms
- **Inputs**: Contract text, historical risk data
- **Outputs**: Risk score, flagged clauses, recommendations
- **Key Features**:
  - Pattern matching for known risk indicators
  - Comparative analysis against safe clauses
  - Confidence scoring for each finding

#### Clause Alignment Agent
- **Purpose**: Ensure consistency across related contracts
- **Inputs**: Current contract, related contracts, clause library
- **Outputs**: Alignment score, inconsistencies, recommended standardizations
- **Key Features**:
  - Vector similarity search for clause matching
  - Cross-contract comparison
  - Standard clause recommendations

#### Obligation Tracking Agent
- **Purpose**: Extract and monitor contractual obligations
- **Inputs**: Contract text, existing obligations database
- **Outputs**: Structured obligations, deadlines, stakeholders
- **Key Features**:
  - Named entity recognition for parties
  - Temporal information extraction
  - Obligation categorization

#### Dependency Graph Agent
- **Purpose**: Map relationships between clauses and obligations
- **Inputs**: Analyzed contracts, extracted clauses
- **Outputs**: Dependency graph, impact analysis
- **Key Features**:
  - Graph construction from clause relationships
  - Cascade impact analysis
  - Visualization support

### 2. Orchestration Layer (LangGraph)

The orchestration layer coordinates agent execution and manages state:

```python
# Pseudo-code for orchestration flow
workflow = StateGraph()

# Add agent nodes
workflow.add_node("risk_analysis", risk_agent.analyze)
workflow.add_node("clause_alignment", clause_agent.analyze)
workflow.add_node("obligation_tracking", obligation_agent.analyze)
workflow.add_node("dependency_graph", dependency_agent.analyze)

# Define execution flow
workflow.set_entry_point("risk_analysis")
workflow.add_edge("risk_analysis", "clause_alignment")
workflow.add_edge("clause_alignment", "obligation_tracking")
workflow.add_edge("obligation_tracking", "dependency_graph")

# Compile and execute
app = workflow.compile()
result = app.invoke(input_data)
```

**Execution Modes**:
- **Sequential**: Agents run in defined order, passing state
- **Concurrent**: Independent agents run in parallel
- **Conditional**: Agent execution based on runtime conditions

### 3. Shared Services Layer

#### LLM Provider Integration
- Abstraction layer for multiple LLM providers (OpenAI, Anthropic)
- Handles API calls, retries, and error handling
- Token counting and cost tracking

#### Vector Store (Supabase)
- Stores contract embeddings for similarity search
- Clause library with pre-defined safe clauses
- Historical contract analysis for context

#### Document Processing Pipeline
```
PDF/DOCX → OCR (Textract) → Text Extraction →
Chunking → Embedding → Vector Storage
```

#### Observability (LangFuse)
- Distributed tracing across all agents
- Prompt logging and response tracking
- Performance metrics and debugging

## Data Flow

### Contract Analysis Flow

1. **Document Ingestion**
   - Upload contract (PDF/DOCX/TXT)
   - OCR processing if needed
   - Text extraction and preprocessing

2. **Embedding Generation**
   - Chunk document into semantic units
   - Generate embeddings using configured model
   - Store in vector database

3. **Agent Orchestration**
   - Distribute contract to relevant agents
   - Execute agents (concurrent or sequential)
   - Collect and aggregate results

4. **Result Synthesis**
   - Combine agent outputs
   - Generate comprehensive analysis report
   - Create explainability traces

5. **Output Delivery**
   - Return structured results to client
   - Store analysis for future reference
   - Log for evaluation and improvement

## Configuration System

The system uses hierarchical configuration:

```
configs/
├── system_config.yaml          # Global system settings
├── agents/
│   ├── risk_agent.yaml        # Agent-specific config
│   ├── clause_agent.yaml
│   ├── obligation_agent.yaml
│   └── dependency_agent.yaml
└── evaluation/
    └── metrics.yaml           # Evaluation configuration
```

Configuration precedence:
1. Environment variables (`.env`)
2. Command-line arguments
3. YAML configuration files
4. Default values in code

## Explainability Architecture

Every agent output includes:

1. **Reasoning Trace**: Step-by-step explanation of analysis
2. **Confidence Scores**: Numerical confidence for each finding
3. **Source References**: Links to specific contract clauses
4. **Alternative Interpretations**: Other possible analyses considered

Example output structure:
```json
{
  "agent_name": "RiskAnalysisAgent",
  "result": {
    "risk_level": "high",
    "findings": [...]
  },
  "confidence": 0.87,
  "reasoning": "The contract contains unlimited liability clause in Section 5.2...",
  "metadata": {
    "clause_references": ["5.2", "7.1"],
    "alternative_interpretations": [...]
  }
}
```

## Scalability Considerations

### Horizontal Scaling
- Agents can be deployed as separate services
- Load balancing across multiple agent instances
- Distributed queue for contract processing

### Vertical Scaling
- Concurrent execution of independent agents
- Batch processing for multiple contracts
- Caching of common clause embeddings

### Performance Optimization
- Lazy loading of agent resources
- Connection pooling for database and API calls
- Response caching for identical queries

## Security Considerations

1. **Data Privacy**: Contracts contain sensitive information
   - Encryption at rest and in transit
   - Access control and audit logging
   - Data retention policies

2. **API Security**: Secure external service integration
   - API key rotation
   - Rate limiting
   - Error handling without information leakage

3. **Prompt Injection**: Prevent malicious inputs
   - Input validation and sanitization
   - Prompt template protection
   - Output filtering

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | LangGraph | Agent coordination |
| LLM | OpenAI GPT-4 / Anthropic Claude | Natural language understanding |
| Vector DB | Supabase (pgvector) | Similarity search |
| OCR | AWS Textract | Document processing |
| Observability | LangFuse | Tracing and monitoring |
| Language | Python 3.11+ | Implementation |
| API Framework | FastAPI | Web interface |

## Future Enhancements

1. **Multi-modal Analysis**: Incorporate charts, tables, signatures
2. **Real-time Collaboration**: Multiple users analyzing same contract
3. **Active Learning**: Agents improve from user feedback
4. **Custom Agent Creation**: User-defined agents for specific needs
5. **Integration APIs**: Connect with CLM platforms (Ironclad, Docusign)

## References

- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- LangFuse Tracing: https://langfuse.com/docs
- Supabase Vector: https://supabase.com/docs/guides/ai
