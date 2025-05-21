import streamlit as st
from models.llm_agent import ask as llm_ask

def advisor_page():
    st.title("AI Financial Advisor")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Advisor:** {message['content']}")
        st.markdown("---")
    
    # Chat input
    user_input = st.text_input("Ask a financial question:")
    if st.button("Send") and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get response from LLM
        response = llm_ask(user_input)
        
        # Add response to chat history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Rerun to update the chat display
        st.experimental_rerun() 