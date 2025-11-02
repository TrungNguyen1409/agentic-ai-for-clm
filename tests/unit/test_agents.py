"""Unit tests for agent implementations."""

import pytest
from src.agents import (
    RiskAnalysisAgent,
    ClauseAlignmentAgent,
    ObligationTrackingAgent,
    DependencyGraphAgent,
)
from src.agents.base import AgentInput, AgentConfig


@pytest.fixture
def sample_contract_text():
    """Sample contract text for testing."""
    return """
    SERVICES AGREEMENT

    1. SERVICES
    Provider shall provide consulting services.

    2. PAYMENT
    Client shall pay $10,000 monthly.

    3. LIABILITY
    Provider's liability is limited to fees paid.
    """


@pytest.fixture
def agent_input(sample_contract_text):
    """Create agent input fixture."""
    return AgentInput(
        contract_text=sample_contract_text,
        metadata={"contract_id": "TEST-001"}
    )


class TestRiskAnalysisAgent:
    """Tests for Risk Analysis Agent."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = RiskAnalysisAgent()
        assert agent.name == "RiskAnalysisAgent"
        assert agent.description is not None

    def test_agent_with_custom_config(self):
        """Test agent with custom configuration."""
        config = AgentConfig(
            name="CustomRiskAgent",
            description="Custom risk agent",
            temperature=0.5
        )
        agent = RiskAnalysisAgent(config)
        assert agent.name == "CustomRiskAgent"
        assert agent.config.temperature == 0.5

    @pytest.mark.asyncio
    async def test_analyze_returns_output(self, agent_input):
        """Test that analyze returns valid output."""
        agent = RiskAnalysisAgent()
        result = await agent.analyze(agent_input)

        assert result.agent_name == agent.name
        assert result.result is not None
        assert 0 <= result.confidence <= 1
        assert result.reasoning is not None

    def test_get_prompt_template(self):
        """Test prompt template is valid."""
        agent = RiskAnalysisAgent()
        template = agent.get_prompt_template()
        assert "{contract_text}" in template
        assert len(template) > 0


class TestClauseAlignmentAgent:
    """Tests for Clause Alignment Agent."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = ClauseAlignmentAgent()
        assert agent.name == "ClauseAlignmentAgent"

    @pytest.mark.asyncio
    async def test_analyze_returns_output(self, agent_input):
        """Test that analyze returns valid output."""
        agent = ClauseAlignmentAgent()
        result = await agent.analyze(agent_input)

        assert result.agent_name == agent.name
        assert "alignment_score" in result.result


class TestObligationTrackingAgent:
    """Tests for Obligation Tracking Agent."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = ObligationTrackingAgent()
        assert agent.name == "ObligationTrackingAgent"

    @pytest.mark.asyncio
    async def test_analyze_returns_output(self, agent_input):
        """Test that analyze returns valid output."""
        agent = ObligationTrackingAgent()
        result = await agent.analyze(agent_input)

        assert result.agent_name == agent.name
        assert "obligations" in result.result


class TestDependencyGraphAgent:
    """Tests for Dependency Graph Agent."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = DependencyGraphAgent()
        assert agent.name == "DependencyGraphAgent"

    @pytest.mark.asyncio
    async def test_analyze_returns_output(self, agent_input):
        """Test that analyze returns valid output."""
        agent = DependencyGraphAgent()
        result = await agent.analyze(agent_input)

        assert result.agent_name == agent.name
        assert "nodes" in result.result
        assert "edges" in result.result
