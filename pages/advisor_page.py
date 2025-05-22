import streamlit as st
from models.llm_agent import ask as llm_ask
from utils.data_processing import load_and_process_data


def get_data_summary(df):
    if df is None or df.empty:
        return "No financial data available."
    # Example summary: top categories, total spend, recent anomalies
    total_spend = df['Amount'].sum()
    top_categories = df['Category'].value_counts().head(3).to_dict() if 'Category' in df.columns else {}
    recent = df.sort_values('Date', ascending=False).head(5)
    summary = f"Total spend: ₹{total_spend:,.0f}. Top categories: {top_categories}. Recent entries: {recent[['Date','Amount','Category']].to_dict(orient='records') if 'Category' in df.columns else recent[['Date','Amount']].to_dict(orient='records')}"
    return summary

def advisor_page():
    st.title("AI Financial Advisor")
    
    # Load processed data
    df = load_and_process_data()
    data_summary = get_data_summary(df)
    
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
        
        # Get response from LLM, passing data context
        response = llm_ask(user_input, data_context=data_summary)
        
        # Add response to chat history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Rerun to update the chat display
        st.experimental_rerun() 