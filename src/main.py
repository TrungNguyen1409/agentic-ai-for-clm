"""Main entry point for the Multi-Agent CLM System."""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any

from src.core.config import settings
from src.agents import (
    RiskAnalysisAgent,
    ClauseAlignmentAgent,
    ObligationTrackingAgent,
    DependencyGraphAgent,
)
from src.agents.base import AgentInput


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def analyze_contract(contract_text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze a contract using all enabled agents.

    Args:
        contract_text: The contract text to analyze
        metadata: Optional metadata about the contract

    Returns:
        Combined analysis results from all agents
    """
    if metadata is None:
        metadata = {}

    logger.info("Starting contract analysis")

    # Prepare input
    agent_input = AgentInput(contract_text=contract_text, metadata=metadata)

    results = {}

    # Initialize and run agents
    agents = []

    if settings.enable_risk_agent:
        logger.info("Initializing Risk Analysis Agent")
        agents.append(("risk_analysis", RiskAnalysisAgent()))

    if settings.enable_clause_agent:
        logger.info("Initializing Clause Alignment Agent")
        agents.append(("clause_alignment", ClauseAlignmentAgent()))

    if settings.enable_obligation_agent:
        logger.info("Initializing Obligation Tracking Agent")
        agents.append(("obligation_tracking", ObligationTrackingAgent()))

    if settings.enable_dependency_agent:
        logger.info("Initializing Dependency Graph Agent")
        agents.append(("dependency_graph", DependencyGraphAgent()))

    # Run agents concurrently
    logger.info(f"Running {len(agents)} agents concurrently")
    agent_tasks = [agent.analyze(agent_input) for _, agent in agents]
    agent_results = await asyncio.gather(*agent_tasks)

    # Combine results
    for (agent_name, _), result in zip(agents, agent_results):
        results[agent_name] = result.model_dump()

    logger.info("Contract analysis complete")
    return results


async def main():
    """Main function for testing the system."""
    logger.info("Multi-Agent CLM System Starting")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"LLM Model: {settings.llm_model}")

    # Sample contract for testing
    sample_contract = """
    SERVICES AGREEMENT

    This Services Agreement ("Agreement") is entered into as of January 1, 2024,
    by and between Company A ("Provider") and Company B ("Client").

    1. SERVICES
    Provider shall provide consulting services as described in Exhibit A.

    2. PAYMENT TERMS
    Client shall pay Provider $10,000 per month, due on the first day of each month.
    Late payments will incur a penalty of 5% per week.

    3. LIABILITY
    Provider's total liability under this Agreement shall not exceed the fees paid
    in the preceding 12 months. Provider makes no warranties, express or implied.

    4. TERMINATION
    Either party may terminate this Agreement with 30 days written notice.
    Upon termination, Client shall pay all outstanding fees immediately.

    5. CONFIDENTIALITY
    Both parties agree to maintain confidentiality of all proprietary information
    disclosed during the term of this Agreement and for 5 years thereafter.
    """

    # Analyze the sample contract
    results = await analyze_contract(
        contract_text=sample_contract,
        metadata={
            "contract_id": "SAMPLE-001",
            "contract_type": "services_agreement",
            "parties": ["Company A", "Company B"],
        },
    )

    # Print results
    print("\n" + "=" * 80)
    print("CONTRACT ANALYSIS RESULTS")
    print("=" * 80)

    for agent_name, result in results.items():
        print(f"\n{agent_name.upper().replace('_', ' ')}:")
        print("-" * 80)
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Result: {result['result']}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
