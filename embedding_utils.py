import google.generativeai as genai
import llm_utils


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


