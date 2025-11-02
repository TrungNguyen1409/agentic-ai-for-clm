"""Unit tests for configuration management."""

import os
import pytest
from src.core.config import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_settings(self):
        """Test default settings are loaded."""
        settings = Settings()
        assert settings.llm_provider in ["openai", "anthropic"]
        assert settings.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]
        assert settings.max_retries >= 0

    def test_supported_formats_list(self):
        """Test supported formats parsing."""
        settings = Settings(supported_formats="pdf,docx,txt")
        formats = settings.supported_formats_list
        assert "pdf" in formats
        assert "docx" in formats
        assert "txt" in formats
        assert len(formats) == 3

    def test_agent_flags(self):
        """Test agent enable/disable flags."""
        settings = Settings(
            enable_risk_agent=True,
            enable_clause_agent=False,
        )
        assert settings.enable_risk_agent is True
        assert settings.enable_clause_agent is False

    def test_vector_settings(self):
        """Test vector database settings."""
        settings = Settings(
            vector_dimension=1536,
            similarity_threshold=0.8
        )
        assert settings.vector_dimension == 1536
        assert 0 <= settings.similarity_threshold <= 1
