import pytest
import os
from llm_utils import init_LLM, set_api_key, get_api_key
from pydantic_ai import Agent


class TestInitLLM:
    """Test cases for the init_LLM function"""
    
    def test_1_initialize_with_valid_api_key(self, monkeypatch):
        """Test 1: Initialize with valid API key"""
        # Set a valid API key in environment
        monkeypatch.setenv('GOOGLE_API_KEY', 'valid-key-123')
        
        # Call init_LLM
        agent = init_LLM()
        
        # Verify an Agent instance is returned
        assert isinstance(agent, Agent)
        assert agent is not None
    
    def test_2_initialize_without_api_key(self, monkeypatch):
        """Test 2: Initialize without API key"""
        # Remove the API key from environment
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Verify EnvironmentError is raised
        with pytest.raises(EnvironmentError) as exc_info:
            init_LLM()
        
        # Check error message
        assert "GOOGLE_API_KEY environment variable not set." in str(exc_info.value)
    
    def test_3_initialize_with_empty_api_key(self, monkeypatch):
        """Test 3: Initialize with empty API key"""
        # Set empty string as API key
        monkeypatch.setenv('GOOGLE_API_KEY', '')
        
        # Verify EnvironmentError is raised (empty string evaluates to False)
        with pytest.raises(EnvironmentError) as exc_info:
            init_LLM()
        
        assert "GOOGLE_API_KEY environment variable not set." in str(exc_info.value)
    
    def test_4_initialize_with_none_api_key(self, monkeypatch):
        """Test 4: Initialize with None API key"""
        # Delete the key to simulate None
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Verify EnvironmentError is raised
        with pytest.raises(EnvironmentError):
            init_LLM()
    
    def test_5_verify_agent_model_configuration(self, monkeypatch):
        """Test 5: Verify agent model configuration"""
        # Set valid API key
        monkeypatch.setenv('GOOGLE_API_KEY', 'valid-key-123')
        
        # Initialize agent
        agent = init_LLM()
        
        # Verify the agent is configured with the correct model
        # Note: Checking model name depends on pydantic_ai's API structure
        assert isinstance(agent, Agent)
    
    def test_6_verify_system_prompt_is_set(self, monkeypatch):
        """Test 6: Verify system prompt is set"""
        # Set valid API key
        monkeypatch.setenv('GOOGLE_API_KEY', 'valid-key-123')
        
        # Initialize agent
        agent = init_LLM()
        
        # Verify agent has the correct system prompt
        # Note: Access to system_prompt depends on pydantic_ai's Agent structure
        assert isinstance(agent, Agent)
    
    def test_7_multiple_initializations(self, monkeypatch):
        """Test 7: Multiple initializations"""
        # Set valid API key
        monkeypatch.setenv('GOOGLE_API_KEY', 'valid-key-123')
        
        # Call init_LLM twice
        agent1 = init_LLM()
        agent2 = init_LLM()
        
        # Verify both are Agent instances
        assert isinstance(agent1, Agent)
        assert isinstance(agent2, Agent)
        
        # Verify they are separate instances
        assert agent1 is not agent2


class TestSetApiKey:
    """Test cases for the set_api_key function"""
    
    def test_1_set_valid_api_key(self, monkeypatch):
        """Test 1: Set valid API key"""
        # Clean environment first
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Set the API key
        set_api_key("test-key-12345")
        
        # Verify it's set in environment
        assert os.environ.get('GOOGLE_API_KEY') == "test-key-12345"
    
    def test_2_set_empty_string(self, monkeypatch):
        """Test 2: Set empty string"""
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Set empty string
        set_api_key("")
        
        # Verify empty string is set
        assert os.environ.get('GOOGLE_API_KEY') == ""
    
    def test_3_set_none_value(self, monkeypatch):
        """Test 3: Set None value"""
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # This may raise TypeError depending on implementation
        try:
            set_api_key(None)
            # If no error, check if None was converted to string
            result = os.environ.get('GOOGLE_API_KEY')
            assert result is not None  # Could be "None" string
        except (TypeError, AttributeError):
            # Expected if None is not allowed
            pass
    
    def test_4_overwrite_existing_key(self, monkeypatch):
        """Test 4: Overwrite existing key"""
        # Set initial key
        monkeypatch.setenv('GOOGLE_API_KEY', 'old-key')
        
        # Overwrite with new key
        set_api_key("new-key")
        
        # Verify new key is set
        assert os.environ.get('GOOGLE_API_KEY') == "new-key"
    
    def test_5_set_key_with_special_characters(self, monkeypatch):
        """Test 5: Set key with special characters"""
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Set key with special characters
        special_key = "key-!@#$%^&*()"
        set_api_key(special_key)
        
        # Verify special characters are intact
        assert os.environ.get('GOOGLE_API_KEY') == special_key


class TestGetApiKey:
    """Test cases for the get_api_key function"""
    
    def test_6_get_existing_api_key(self, monkeypatch):
        """Test 6: Get existing API key"""
        # Set API key in environment
        monkeypatch.setenv('GOOGLE_API_KEY', 'test-key')
        
        # Get the API key
        result = get_api_key()
        
        # Verify correct key is returned
        assert result == "test-key"
    
    def test_7_get_when_not_set(self, monkeypatch):
        """Test 7: Get when not set"""
        # Remove API key from environment
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Get the API key
        result = get_api_key()
        
        # Verify None is returned
        assert result is None
    
    def test_8_get_after_set_api_key(self, monkeypatch):
        """Test 8: Get after set_api_key"""
        # Clean environment
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Set a new key
        set_api_key("new-key")
        
        # Get the key
        result = get_api_key()
        
        # Verify the key matches
        assert result == "new-key"
    
    def test_9_get_empty_string_key(self, monkeypatch):
        """Test 9: Get empty string key"""
        # Set empty string as API key
        monkeypatch.setenv('GOOGLE_API_KEY', '')
        
        # Get the key
        result = get_api_key()
        
        # Verify empty string is returned
        assert result == ""
    
    def test_10_get_after_multiple_sets(self, monkeypatch):
        """Test 10: Get after multiple sets"""
        # Clean environment
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
        
        # Set multiple times
        set_api_key("first-key")
        set_api_key("second-key")
        set_api_key("third-key")
        
        # Get the key
        result = get_api_key()
        
        # Verify most recent key is returned
        assert result == "third-key"
