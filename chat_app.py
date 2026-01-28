import streamlit as st
import os
import logging
from datetime import datetime
from llm_utils import init_LLM
from pdf_utils import extract_text_from_pdf
from chromadb_utils import store_text_as_document, search_document_by_text, get_all_document_filenames
import llm_utils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("="*50)
logger.info("Starting Personal Knowledge Genie application")
logger.info("="*50)

try:
    agent = init_LLM()
    logger.info("LLM agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM agent: {str(e)}")
    raise

def main():
    logger.info("Main function started")
    
    st.set_page_config(
        page_title="Personal Knowledge Genie",
        page_icon="🧠",
        layout="wide"
    )
    logger.debug("Streamlit page configuration set")
    
    st.title("🧠 Personal Knowledge Genie")
    
    # Create two columns for the layout
    left_panel, right_panel = st.columns([1, 2])
    
    # Left Panel - File Upload
    with left_panel:
        st.header("📁 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Upload your documents",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF or text files to add to your knowledge base "
        )
        
        # show all the documents already in ChromaDB using chromadb_utils
        logger.info("Fetching all documents from knowledge base")
        filenames = get_all_document_filenames()
        logger.info(f"Retrieved {len(filenames) if filenames else 0} documents from knowledge base")
        if filenames:
            st.subheader("Documents in Knowledge Base: ")
            for filename in filenames:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {filename}")
                with col2:
                    if st.button("🗑️", key=f"delete_{filename}", help=f"Delete {filename}"):
                        logger.info(f"Delete button clicked for document: {filename}")
                        with st.spinner(f"Deleting {filename}..."):
                            try:
                                from chromadb_utils import delete_document_by_filename
                                logger.info(f"Attempting to delete document: {filename}")
                                delete_document_by_filename(filename)
                                logger.info(f"Successfully deleted document: {filename}")
                                st.success("✅")
                                st.rerun()
                            except Exception as e:
                                logger.error(f"Error deleting document {filename}: {str(e)}", exc_info=True)
                                st.error(f"❌ Error deleting {filename}: {str(e)}")

        if uploaded_files:
            logger.info(f"User uploaded {len(uploaded_files)} file(s)")
            st.subheader("Uploaded Files:")
            for file in uploaded_files:
                logger.debug(f"Uploaded file: {file.name} (type: {file.type}, size: {file.size} bytes)")
                st.write(f"• {file.name}")
                
                # Process and store the file
                if st.button(f"Process {file.name}", key=f"process_{file.name}"):
                    logger.info(f"Processing started for file: {file.name}")
                    with st.spinner(f"Processing {file.name}..."):
                        try:
                            if file.type == "application/pdf":
                                logger.info(f"Processing PDF file: {file.name}")
                                # Save the uploaded file temporarily
                                temp_path = f"temp_{file.name}"
                                logger.debug(f"Saving temporary file: {temp_path}")
                                with open(temp_path, "wb") as f:
                                    f.write(file.getbuffer())
                                logger.debug(f"Temporary file saved: {temp_path}")
                                
                                # Extract text from PDF
                                logger.info(f"Extracting text from PDF: {file.name}")
                                text = extract_text_from_pdf(temp_path)
                                logger.info(f"Successfully extracted {len(text)} characters from {file.name}")
                                
                                # Clean up temp file
                                logger.debug(f"Removing temporary file: {temp_path}")
                                os.remove(temp_path)
                                logger.debug(f"Temporary file removed: {temp_path}")
                                
                            elif file.type == "text/plain":
                                logger.info(f"Processing text file: {file.name}")
                                # Read text file
                                text = str(file.read(), "utf-8")
                                logger.info(f"Successfully read {len(text)} characters from text file: {file.name}")
                            
                            # Store in ChromaDB
                            logger.info(f"Storing document in ChromaDB: {file.name}")
                            doc_id = store_text_as_document(
                                text, 
                                metadata={"filename": file.name, "file_type": file.type}
                            )
                            logger.info(f"Document stored successfully with ID: {doc_id} for file: {file.name}")
                            
                            st.success(f"✅ {file.name} processed and stored successfully!")
                            st.info(f"Document ID: {doc_id}")
                            
                        except Exception as e:
                            logger.error(f"Error processing file {file.name}: {str(e)}", exc_info=True)
                            st.error(f"❌ Error processing {file.name}: {str(e)}")
    
    # Right Panel - Chat Interface
    with right_panel:
        st.header("💬 Chat with Your Documents")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            logger.info("Initializing new chat session")
            st.session_state.messages = []
        else:
            logger.debug(f"Chat session has {len(st.session_state.messages)} messages")
        

        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your documents..."):
            logger.info(f"User query received: {prompt[:100]}...")  # Log first 100 chars
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Search for relevant documents
                        logger.info("Searching knowledge base for relevant documents")
                        search_results = search_document_by_text(prompt)
                        logger.info(f"Search completed. Found {len(search_results.get('documents', [[]])[0])} relevant chunks")
                        # logger.info("Search result: "+ str(search_results))
                        
                        # Prepare context from search results
                        context = ""
                        if search_results["documents"] and search_results["documents"][0]:
                            context = "\n".join(search_results["documents"][0][:3])  # Top 3 results
                            logger.info(f"Using top 3 search results as context ({len(context)} chars)")
                        else:
                            logger.warning("No relevant documents found in search results")
                        
                        # Create prompt with context
                        full_prompt = f"""
                        Context from documents:
                        {context}
                        
                        User question: {prompt}

                        Please answer the question based on the context provided. If the context doesn't contain relevant information, say so.
                        """ 
                        
                        # Get response from LLM
                        logger.info("Requesting response from LLM agent: "+ full_prompt)

                        response = llm_utils.get_agent_response(agent, full_prompt)
                        logger.info(f"LLM response received ({len(response.output)} chars)")
                        
                        st.markdown(response.output)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response.output})
                        logger.debug("Response added to chat history")
                        
                    except Exception as e:
                        logger.error(f"Error generating chat response: {str(e)}", exc_info=True)
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
                # Display chat messages
        
        
        # Show chat history
        chat_container = st.container()
        with chat_container:
            st.markdown("### Chat History  ###")
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            logger.info("Clearing chat history")
            st.session_state.messages = []
            logger.info("Chat history cleared, rerunning app")
            st.rerun()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error in main application: {str(e)}", exc_info=True)
        raise