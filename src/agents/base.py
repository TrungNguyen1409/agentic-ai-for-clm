"""Base agent class for all specialized contract analysis agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    name: str = Field(description="Agent name")
    description: str = Field(description="Agent description")
    llm_model: str = Field(default="gpt-4-turbo-preview", description="LLM model to use")
    temperature: float = Field(default=0.0, description="LLM temperature")
    max_tokens: int = Field(default=2000, description="Maximum tokens for response")
    enable_tracing: bool = Field(default=True, description="Enable LangFuse tracing")


class AgentInput(BaseModel):
    """Base input for agent execution."""

    contract_text: str = Field(description="Contract text to analyze")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AgentOutput(BaseModel):
    """Base output from agent execution."""

    agent_name: str = Field(description="Name of the agent")
    result: Dict[str, Any] = Field(description="Analysis results")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    reasoning: str = Field(description="Reasoning trace for explainability")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class BaseAgent(ABC):
    """Abstract base class for all contract analysis agents."""

    def __init__(self, config: AgentConfig):
        """
        Initialize the agent.

        Args:
            config: Agent configuration
        """
        self.config = config
        self.name = config.name
        self.description = config.description

    @abstractmethod
    async def analyze(self, input_data: AgentInput) -> AgentOutput:
        """
        Analyze contract data and return results.

        Args:
            input_data: Input data for analysis

        Returns:
            Analysis results with reasoning trace
        """
        pass

    @abstractmethod
    def get_prompt_template(self) -> str:
        """
        Get the prompt template for this agent.

        Returns:
            Prompt template string
        """
        pass

    def format_prompt(self, input_data: AgentInput) -> str:
        """
        Format the prompt with input data.

        Args:
            input_data: Input data

        Returns:
            Formatted prompt
        """
        template = self.get_prompt_template()
        return template.format(
            contract_text=input_data.contract_text,
            **input_data.metadata
        )
