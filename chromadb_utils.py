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

# write a function to search for a text and return matching documents
def search_document_by_text(text, collection_name="documents"):
    """
    Searches for documents in ChromaDB by their content.
    Args:
        text (str): The text content to search for.
        collection_name (str): Name of the collection to search in.
    Returns:
        list: A list of matching document metadata.
    """
    # Create a ChromaDB client
    client = chromadb.Client()

    # Get the collection
    collection = client.get_collection(name=collection_name)

    # Search for documents by content
    results = collection.query(documents=[text])
    return results


# sample usage
if __name__ == "__main__":
    doc_id = store_text_as_document("Hello, world!")
    print(f"Stored document with ID: {doc_id}")
    results = search_document_by_text("Hello, world!")
    print(f"Search results: {results}")
    