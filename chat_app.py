import streamlit as st
import os
from llm_utils import init_LLM
from pdf_utils import extract_text_from_pdf
from chromadb_utils import store_text_as_document, search_document_by_text, get_all_document_filenames
import llm_utils

agent = init_LLM()

def main():  
    st.set_page_config(
        page_title="Personal Knowledge Genie",
        page_icon="🧠",
        layout="wide"
    )
    
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
        filenames = get_all_document_filenames()
        if filenames:
            st.subheader("Documents in Knowledge Base: ")
            for filename in filenames:
                st.write(f"• {filename}")

        if uploaded_files:
            st.subheader("Uploaded Files:")
            for file in uploaded_files:
                st.write(f"• {file.name}")
                
                # Process and store the file
                if st.button(f"Process {file.name}", key=f"process_{file.name}"):
                    with st.spinner(f"Processing {file.name}..."):
                        try:
                            if file.type == "application/pdf":
                                # Save the uploaded file temporarily
                                temp_path = f"temp_{file.name}"
                                with open(temp_path, "wb") as f:
                                    f.write(file.getbuffer())
                                
                                # Extract text from PDF
                                text = extract_text_from_pdf(temp_path)
                                
                                # Clean up temp file
                                os.remove(temp_path)
                                
                            elif file.type == "text/plain":
                                # Read text file
                                text = str(file.read(), "utf-8")
                            
                            # Store in ChromaDB
                            doc_id = store_text_as_document(
                                text, 
                                metadata={"filename": file.name, "file_type": file.type}
                            )
                            
                            st.success(f"✅ {file.name} processed and stored successfully!")
                            st.info(f"Document ID: {doc_id}")
                            
                        except Exception as e:
                            st.error(f"❌ Error processing {file.name}: {str(e)}")
    
    # Right Panel - Chat Interface
    with right_panel:
        st.header("💬 Chat with Your Documents")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        

        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your documents..."):
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
                        search_results = search_document_by_text(prompt)
                        
                        # Prepare context from search results
                        context = ""
                        if search_results["documents"] and search_results["documents"][0]:
                            context = "\n".join(search_results["documents"][0][:3])  # Top 3 resultss
                        
                        # Create prompt with context
                        full_prompt = f"""
                        Context from documents:
                        {context}
                        
                        User question: {prompt}

                        Please answer the question based on the context provided. If the context doesn't contain relevant information, say so.
                        """
                        
                        # Get response from LLM
                        response = llm_utils.get_agent_response(agent, full_prompt)
                        
                        st.markdown(response.output)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response.output})
                        
                    except Exception as e:
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
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()