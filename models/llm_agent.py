import os
from dotenv import load_dotenv

load_dotenv()

# Simple mock function for the advisor
def ask(user_input, data_context=None, user_id="default_user", stream_handler=None):
    """Process a user query and return the LLM response, using data_context if provided"""
    if data_context:
        prompt = f"Financial Data Context: {data_context}\n\nUser Question: {user_input}"
    else:
        prompt = user_input
    # If using a real LLM, pass prompt to the chain. For now, use the mock logic:
    # chain = get_llm_chain()
    # return chain.invoke({"input": prompt}, config={"configurable": {"session_id": user_id}})
    # Mock logic below:
    if 'forecast' in prompt.lower():
        return "Based on your current financial data, I forecast a 12% increase in revenue over the next quarter if current trends continue. Would you like me to analyze specific expense categories?"
    elif 'expense' in prompt.lower() or 'spending' in prompt.lower():
        return "Your highest expense categories are Marketing (32%), Engineering (28%), and Admin (18%). There's an opportunity to optimize Marketing spend which has increased 15% over the last quarter."
    elif 'anomaly' in prompt.lower() or 'fraud' in prompt.lower():
        return "I've detected 3 potential anomalies in your recent transactions. The most significant is a ₹411,492 payment to Google on May 23rd, which is 10x larger than your typical Google payments."
    elif 'runway' in prompt.lower() or 'burn' in prompt.lower():
        return "At your current burn rate of approximately ₹2.5M per month, your runway is estimated at 4.2 months. I recommend reviewing your SaaS subscriptions which have increased by 22% this quarter."
    else:
        return "I can help answer questions about your financial data, including expense analysis, anomaly detection, forecasting, and runway calculations. What specific aspect would you like insights on?"

# LLM setup - placeholder for future implementation
FINANCE_ADVISOR_PROMPT = '''
You are a specialized AI financial advisor created exclusively to assist a startup by analyzing its expenditure reports, forecasting data, and anomaly detection results. You will be given parsed data from internal financial tools and are expected to provide actionable, clear, and accurate financial advice based on that input.

Your responsibilities:
1. Only respond to finance-related queries about the startup's financial health
2. Use only provided financial data (no speculation)
3. Structure responses:
   - Insight: Financial insight from data
   - Reasoning: Why it matters (with numbers/trends)
   - Advice: Specific next steps
4. Reject non-finance questions with: "I'm designed solely for financial guidance."
5. Never engage in small talk or off-topic discussions
6. Include projections when forecasting data is mentioned
7. Highlight risks when anomaly data is referenced
8. If data is missing: "I need more specific financial data."

Respond only based on provided financial data.
'''

def initialize_llm():
    """Initialize the LLM and return the chain"""
    llm = ChatOllama(base_url=BASE_URL, model=MODEL, temperature=0.3)  # Lower temp for more focused responses

    # Prompt setup
    system_prompt = SystemMessagePromptTemplate.from_template(FINANCE_ADVISOR_PROMPT)
    human_prompt = HumanMessagePromptTemplate.from_template("{input}")
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    chain = chat_prompt | llm | StrOutputParser()

    return chain

def get_llm_chain():
    """Get or create the LLM chain"""
    if 'llm_chain' not in st.session_state:
        st.session_state.llm_chain = initialize_llm()
    return st.session_state.llm_chain

def ask(user_input, user_id="default_user", stream_handler=None):
    """Process a user query and return the LLM response
    
    Args:
        user_input (str): The user's query
        user_id (str): User identifier for chat history
        stream_handler (callable, optional): Function to handle streaming responses
        
    Returns:
        str: The LLM's response
    """
    chain = get_llm_chain()
    
    runnable_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    if stream_handler:
        # Stream the response through the handler
        full_response = ""
        for chunk in runnable_with_history.stream(
            {"input": user_input},
            config={"configurable": {"session_id": user_id}}
        ):
            full_response += chunk
            stream_handler(full_response)
        return full_response
    else:
        # Return the complete response at once
        return runnable_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": user_id}}
        )

def create_standalone_ui():
    """Create a standalone UI for the LLM agent when run directly"""
    st.set_page_config(layout="wide", page_title="Financial Advisor Chatbot")
    st.title("Financial Advisory Assistant")
    st.write("I specialize in analyzing your startup's financial data. How can I help?")
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # User ID handling
    user_id = st.text_input("Enter your user ID", "default_user")
    if not user_id.strip():
        st.warning("Please enter a valid user ID")
        st.stop()
    
    # New conversation button
    if st.button("Start New Conversation"):
        st.session_state.chat_history = []
        history = get_session_history(user_id)
        history.clear()
        st.experimental_rerun()  # Use experimental_rerun for Streamlit 1.8.0
    
    # Display chat history
    for idx, message in enumerate(st.session_state.chat_history):
        role = message['role']
        content = message['content']
        
        if role == 'user':
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**Advisor:** {content}")
        st.markdown("---")
    
    # Chat interface
    prompt = st.text_input("Ask a finance-related question:", key="finance_question")
    if st.button("Send", key="send_question") or prompt:
        if prompt:  # Check if prompt is not empty
            # Add user message to chat
            st.session_state.chat_history.append({'role': 'user', 'content': prompt})
            
            # Get response
            with st.spinner("Thinking..."):
                # Simple update function that doesn't use streaming
                def update_response(text):
                    pass  # Not using streaming in this version
                
                full_response = ask(prompt, user_id, None)  # Don't use streaming
            
            # Add assistant response to history
            st.session_state.chat_history.append({'role': 'assistant', 'content': full_response})
            
            # Rerun to show updated chat
            st.experimental_rerun()

# Run the standalone UI if this file is executed directly
if __name__ == "__main__":
    create_standalone_ui()