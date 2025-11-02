"""Risk Analysis Agent for detecting red-flag clauses and liability gaps."""

from typing import Dict, Any
from .base import BaseAgent, AgentConfig, AgentInput, AgentOutput


class RiskAnalysisAgent(BaseAgent):
    """
    Agent responsible for analyzing contracts to identify:
    - Red-flag clauses
    - Liability gaps
    - Unbalanced terms
    - Financial risk indicators
    """

    def __init__(self, config: AgentConfig | None = None):
        """Initialize Risk Analysis Agent."""
        if config is None:
            config = AgentConfig(
                name="RiskAnalysisAgent",
                description="Detects red-flag clauses, liability gaps, and unbalanced terms",
                temperature=0.1,
            )
        super().__init__(config)

    async def analyze(self, input_data: AgentInput) -> AgentOutput:
        """
        Analyze contract for risk factors.

        Args:
            input_data: Contract text and metadata

        Returns:
            Risk analysis results with confidence and reasoning
        """
        # TODO: Implement actual risk analysis logic
        # This is a placeholder for the prototype phase

        result = {
            "risk_level": "medium",
            "red_flags": [],
            "liability_gaps": [],
            "recommendations": []
        }

        return AgentOutput(
            agent_name=self.name,
            result=result,
            confidence=0.0,
            reasoning="Placeholder implementation - to be developed in Phase 2",
        )

    def get_prompt_template(self) -> str:
        """Get the risk analysis prompt template."""
        return """
You are a Risk Analysis Agent specialized in contract review.

Analyze the following contract text and identify:
1. Red-flag clauses (e.g., unlimited liability, unfair termination terms)
2. Liability gaps (missing indemnification, warranty limitations)
3. Unbalanced terms (one-sided obligations)
4. Financial risk indicators (payment terms, penalties)

Contract Text:
{contract_text}

Provide your analysis in the following structure:
- Overall risk level (low/medium/high)
- Specific red flags with clause references
- Identified liability gaps
- Actionable recommendations

Be specific and reference exact clauses where possible.
"""
