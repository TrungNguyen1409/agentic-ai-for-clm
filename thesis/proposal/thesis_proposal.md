# Master's Thesis Proposal

**Title:** Design and Evaluation of Multi-Agentic AI Systems for Contract Lifecycle Management SaaS Platforms

**Author:** Trung Nguyen
**Supervisor:** Prof. Dr. Ingo Weber
**Advisor:** MS Samed Bayer
**Submission Date:** April 2026

---

## Motivation

In recent years, Contract Lifecycle Management (CLM) has increasingly adopted artificial intelligence to automate tasks such as clause extraction, risk scoring, and contract summarization. These advancements demonstrate the potential of AI-driven CLM systems to reduce manual workload and accelerate contract turnaround times. However, current solutions typically rely on monolithic, single-agent large language models (LLMs) that offer limited explainability, weak controllability, high hallucination risk, and poor scalability across diverse contract types and jurisdictions. Such black-box architectures make it difficult to ensure consistency, traceability, and compliance—capabilities that are critical in regulated, multi-stakeholder enterprise environments.

Multi-agent systems (MAS) have recently emerged as a promising paradigm for addressing these limitations. By decomposing contract workflows into specialized, collaborating agents, MAS can enable modular scalability, explicit reasoning chains, and improved explainability. Despite this potential, their application to enterprise CLM remains largely unexplored. Existing studies highlight a clear research gap: the absence of frameworks and empirical evaluation for compliance-aware, explainable multi-agent orchestration in enterprise contract management.

## Research Questions

**Main Question:**
How can a multi-agent framework be designed and implemented to improve contract analysis efficiency, accuracy, and explainability in enterprise CLM systems?

**Sub-questions:**
- What agent specialization patterns are most effective for contract analysis tasks (drafting, review, compliance checking)?
- How does a multi-agent approach compare to single-agent systems in contract analysis accuracy and processing time?
- What explainability mechanisms are most effective for multi-agent contract analysis systems to ensure transparency and trust in enterprise environments?

## Research Objectives

1. Design a focused multi-agent framework for contract analysis based on industry foundation papers
2. Develop a working prototype with 2-3 specialized agents
3. Conduct comparative evaluation using real contract data
4. Establish practical implementation guidelines for enterprise CLM integration

## Methodology

### Foundation Framework Design

Grounded in domain expertise from enterprise and construction contract management, this research identifies four key agent roles that address practical challenges in Contract Lifecycle Management (CLM):

1. **Risk Analysis Agent** – detects red-flag clauses, liability gaps, and unbalanced terms during contract drafting
2. **Clause Alignment Agent** – ensures consistency across interrelated project contracts by recommending standardized or back-to-back clauses from the clause library
3. **Obligation Tracking Agent** – monitors post-signature obligations and deadlines across stakeholders to improve compliance
4. **Dependency Graph Agent** (forward-looking) – maintains a dynamic representation of clause and obligation relationships across multiple contracts

To identify and refine these roles, the research will conduct interviews with CLM practitioners and analyze documented pain points from large-scale construction projects. The multi-agent architecture will be designed following established MAS principles (e.g., Wooldridge's frameworks) and enterprise AI orchestration patterns, focusing on modularity, explainability, and compliance awareness.

### Prototype Implementation

A working prototype will operationalize the designed architecture using modern agentic AI frameworks. Core components include:

1. **Inter-agent communication and orchestration** implemented through LangGraph, enabling concurrent, event-driven collaboration among specialized agents
2. **A contract processing pipeline** leveraging AWS Textract and custom OCR pipeline for document parsing, clause extraction, and retrieval-augmented reasoning using vector embeddings stored in Supabase's vector database
3. **Built-in explainability and observability** through LangFuse, providing detailed reasoning traces, confidence scores, and user-level audit logs
4. **A lightweight web interface** for interactive testing of agent behavior and real-time contract analysis scenarios

The prototype will be developed in Python, integrating existing LLM APIs (e.g., GPT-4 or similar models) for natural language understanding and leveraging asynchronous orchestration within the LangGraph framework to simulate enterprise-grade agent workflows.

### Evaluation and Validation

The evaluation will assess the proposed multi-agent framework across three dimensions:

1. **Efficiency and Accuracy** – Comparative study against single-agent LLM and traditional non-LLM baselines (e.g., rule-based systems, ML classifiers) using precision, recall, and F1 metrics for risk detection, and overall processing time for efficiency measurement

2. **Consistency and Compliance** – Testing how well the system maintains consistency across related contracts and accurately tracks obligations and deadlines

3. **Explainability and Trust** – Qualitative assessment using reasoning-trace coverage, auditability through LangFuse logs, and expert interviews evaluating clarity and reliability

## Timeline & Risks

The research project spans from October 2025 to March 2026, structured into three phases with dedicated time for thesis writing.

### Phase 1: Literature Review + Detailed Planning (October - November 2025)
- Study multi-agent systems and enterprise AI frameworks
- Design multi-agent architecture for contract analysis (2-3 specialized agents)
- Define agent roles, communication protocols, and system requirements

### Phase 2: Prototype Implementation (December 2025 - January 2026)
- Develop working prototype using relevant agentic frameworks and libraries
- Implement modular architecture with JSON/YAML configuration files
- Establish agent reasoning pipeline and basic explainability features
- Key: Avoid hard-coded features; use configurable parameters for easy experimentation

### Phase 3: Evaluation and Validation (February - March 2026)
- Conduct comparative evaluation using real contract datasets
- Test multi-agent system against single-agent baseline
- Thesis Writing: Reserve final 3-4 weeks for writing and quick fixes

### Milestones

- **November 2025:** Framework design complete, agent roles defined
- **January 2026:** Working prototype with core functionality achieved
- **March 2026:** Evaluation complete, thesis writing finished

## Technical Risks and Mitigation

### Key Technical Risks

1. **Agent Coordination** – Communication overhead between agents reducing system efficiency
2. **Framework Integration** – Challenges integrating LangGraph, LangChain, and Supabase
3. **Data Quality** – Limited access to high-quality contract datasets for training and evaluation
4. **Evaluation Validity** – Risk of poor evaluation results due to insufficient or low-quality testing data

### Mitigation Strategies

1. **Modular Architecture** – Implement configurable agent communication protocols for easy adjustment
2. **Incremental Development** – Build and test components individually before full integration
3. **Dataset Preparation** – Use CUAD dataset and synthetic data generation if needed
4. **Evaluation Planning** – Design evaluation framework early and validate data quality before testing

## Expected Contributions

1. Working prototype implementation with documented architecture, agent design patterns, and integration approach for enterprise CLM systems
2. Evaluation framework and metrics for assessing multi-agent contract analysis systems, with practical guidelines for implementation
3. Practical explainability features for enterprise contract analysis, validated through user testing and trust assessment

**Impact Areas:** Contract analysis automation, Multi-Agent Systems in enterprise software, Legal Technology prototyping, and practical AI implementation patterns.

## References

[BÇ25] - Hallucination risks in LLMs
[Bil+23] - Contract analysis challenges
[Xia+25] - Multi-jurisdiction contract systems
[GR21] - Enterprise compliance requirements
[Wan+24a] - Multi-stakeholder CLM environments
[Shu+24] - Multi-agent system architectures
[Wan+24b] - Agent collaboration patterns
[WY25] - Explainability in MAS
[Yeh+25] - CLM framework gaps
[Kar25] - Compliance-aware AI systems
[Wik25] - Contract Lifecycle Management overview
