import google.generativeai as genai
import llm_utils

# Configure Google Generative AI with API key from llm_utils
api_key = llm_utils.get_api_key()
if api_key:
    genai.configure(api_key=api_key)
else:
    raise EnvironmentError("API key not found. Please set it using llm_utils.set_api_key()")


def get_text_embedding(text):
    """
    Takes a text input and returns its embedding using Google's embedding model.
    Args:
        text (str): The text to embed.
    Returns:
        list: The embedding vector for the text.
    """
    # Generate embedding using the correct method
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return result['embedding']


