import chromadb
import uuid
import os
from datetime import datetime


def store_text_as_document(text, collection_name="documents", metadata=None):
    """
    Stores text as a document in ChromaDB.
    Args:
        text (str): The text content to store.
        collection_name (str): Name of the collection to store the document in.
        metadata (dict): Optional metadata to associate with the document.
    Returns:
        str: The ID of the stored document.
    """
    # Create vectordb directory if it doesn't exist
    vectordb_path = os.path.join(os.path.dirname(__file__), "vectordb")
    os.makedirs(vectordb_path, exist_ok=True)
    
    # Create a persistent ChromaDB client
    client = chromadb.PersistentClient(path=vectordb_path)
    
    # Get or create a collection
    collection = client.get_or_create_collection(name=collection_name)
    
    # Generate a unique ID for the document
    doc_id = str(uuid.uuid4())
    
    # Add timestamp to metadata if not provided
    if metadata is None:
        metadata = {}
    metadata["timestamp"] = datetime.now().isoformat()
    
    # Add the document to the collection
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id]
    )
    
    return doc_id


# sample usage
if __name__ == "__main__":
    doc_id = store_text_as_document("Hello, world!")
    print(f"Stored document with ID: {doc_id}")