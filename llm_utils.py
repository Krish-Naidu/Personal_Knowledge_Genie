from pydantic_ai import Agent
# Import os to access environment variables for API key
import os


# Set up the Google API key for Gemini model
# You can set this as an environment variable: GOOGLE_API_KEY
# Or replace "your-google-api-key-here" with your actual API key
def init_LLM():
    set_api_key("AIzaSyAT-xzR1hSHM4IG5HUlVRk8wgRYXJFUCR8") 
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")
    os.environ['GOOGLE_API_KEY'] = api_key
    # Create an AI agent instance with specific configuration
    agent = Agent(
        'google-gla:gemini-2.5-flash-lite',
        system_prompt='Be concise, reply with one sentence.',
    )
    return agent


def get_agent_response(agent, input_text):
    """
    Takes a string input and returns the response from the agent's run_sync method.
    Args:
        input_text (str): The input string to send to the agent.
    Returns:
        str: The agent's response.
    """
    return agent.run_sync(input_text)


def set_api_key(api_key):
    """
    Sets the provided API key to the OS environment variable 'GOOGLE_API_KEY'.
    Args:
        api_key (str): The API key to set.
    """
    os.environ['GOOGLE_API_KEY'] = api_key

def get_api_key():
    """
    Retrieves the API key from the OS environment variable 'GOOGLE_API_KEY'.
    Returns:
        str: The API key if set, else None.
    """
    return os.environ.get('GOOGLE_API_KEY')

 # Replace with your actual API key or set the environment variable


# sample usage
if __name__ == "__main__":
    agent = init_LLM()
    response = get_agent_response(agent, "What is the capital of France?")
    print(response)