from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import os
from pathlib import Path
import json
from datetime import datetime
import plotly.graph_objects as go
from langchain_core.prompts import (
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate, 
    ChatPromptTemplate
)
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

load_dotenv('./../.env')

# Base settings for the chatbot
base_url = "http://localhost:11434"
model = 'tinyllama:latest'

# Financial advisor system prompt
financial_advisor_prompt = '''
You are a professional financial advisor designed to provide comprehensive financial guidance. Your role is to:

1. Analyze financial questions and provide detailed, actionable advice
2. Maintain a professional and clear communication style
3. Focus on practical, implementable solutions
4. Consider both short-term and long-term financial implications
5. Provide balanced and responsible financial recommendations

You must follow these guidelines:

1. Always maintain a professional tone
2. Provide specific, actionable advice
3. Include relevant financial considerations
4. Explain complex concepts in clear terms
5. Consider risk factors in recommendations
6. Suggest practical next steps
7. Include relevant financial metrics when applicable
8. Reference industry best practices
9. Consider regulatory and compliance aspects
10. Maintain ethical standards in all advice

Your responses should be:
- Clear and concise
- Well-structured
- Professional
- Actionable
- Educational
- Balanced
- Risk-aware
- Compliance-conscious

Remember to:
- Focus on the user's specific financial situation
- Provide context for recommendations
- Include relevant financial metrics
- Suggest practical implementation steps
- Consider both opportunities and risks
- Reference industry standards
- Maintain professional boundaries
- Prioritize user's financial well-being

Respond to financial queries with comprehensive, professional advice that helps users make informed financial decisions.
'''

class AIAdvisor:
    def __init__(self):
        self.chat_history = []
        self.load_chat_history()
        self.setup_chain()
    
    def setup_chain(self):
        """Setup the financial advisor chain"""
        # Create prompt template
        system_message = SystemMessagePromptTemplate.from_template(financial_advisor_prompt)
        human_message = HumanMessagePromptTemplate.from_template("{input}")
        prompt = ChatPromptTemplate.from_messages([system_message, human_message])
        
        # Setup LLM
        llm = ChatOllama(base_url=base_url, model=model)
        
        # Create chain
        self.chain = prompt | llm | StrOutputParser()
    
    def load_chat_history(self):
        """Load chat history from file"""
        chat_file = Path("data/chat_history/chat.json")
        if chat_file.exists():
            try:
                with open(chat_file, 'r') as f:
                    self.chat_history = json.load(f)
            except Exception as e:
                st.warning(f"Could not load chat history: {str(e)}")
                self.chat_history = []
    
    def save_chat_history(self):
        """Save chat history to file"""
        chat_file = Path("data/chat_history/chat.json")
        try:
            with open(chat_file, 'w') as f:
                json.dump(self.chat_history, f)
        except Exception as e:
            st.warning(f"Could not save chat history: {str(e)}")
    
    def generate_response(self, input_text, username=None):
        """Generate response using the financial advisor chain"""
        # Add personalization if username is provided
        if username:
            input_text = f"User {username} asks: {input_text}"
        
        # Generate response
        response = self.chain.invoke({"input": input_text})
        return response
    
    def render(self):
        """Render the financial advisor interface"""
        st.subheader("Financial Advisory System")
        
        # Add guide card
        with st.expander("Financial Advisory Guide", expanded=True):
            st.markdown("""
            ### Financial Advisory System
            
            **Available Services:**
            - Financial Analysis and Planning
            - Investment Strategy
            - Risk Management
            - Budgeting and Saving
            - Debt Management
            - Retirement Planning
            - Tax Planning
            - Estate Planning
            
            **Example Inquiries:**
            - "How should I plan for retirement?"
            - "What's the best way to manage my investments?"
            - "How can I improve my credit score?"
            - "What are good saving strategies?"
            - "How should I plan my taxes?"
            """)
        
        # Get username
        username = st.text_input("Enter your name for personalized advice", "")
        
        # Display chat history
        for message in self.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Enter your financial inquiry"):
            # Add user message to chat
            self.chat_history.append({"role": "user", "content": prompt})
            
            # Generate and display response
            with st.chat_message("assistant"):
                response = self.generate_response(prompt, username)
                st.write(response)
                self.chat_history.append({"role": "assistant", "content": response})
            
            # Save chat history
            self.save_chat_history()
        
        # Add clear chat button
        if st.button("Reset Conversation"):
            self.chat_history = []
            self.save_chat_history()
            st.experimental_rerun()

# Only run the Streamlit UI code if this file is run directly
if __name__ == "__main__":
    # Set page config
    st.set_page_config(layout="wide")
    
    # Initialize the advisor
    advisor = AIAdvisor()
    advisor.render()

