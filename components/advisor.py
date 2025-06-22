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
import logging

load_dotenv('./../.env')

# Base settings for the chatbot
base_url = "http://localhost:11434"
model = 'tinyllama:latest'

# Financial advisor system prompt (updated for generic chatbot)
financial_advisor_prompt = '''
You are a professional financial assistant chatbot for a business. You can:

1. Answer general financial questions and provide advice
2. Run financial forecasts on the company's transaction data
3. Detect anomalies (unusual transactions) in the company's transaction data

You have access to the company's financial data (uploaded as a CSV), and can use advanced tools to:
- Predict future spending (forecasting)
- Find unusual or suspicious transactions (anomaly detection)

If the user asks for a forecast, prediction, or future trend, run the forecasting tool and show the results (including charts and summaries).
If the user asks about anomalies, unusual transactions, or suspicious activity, run the anomaly detection tool and show the results (including tables and summaries).
For all other questions, answer as a helpful, professional financial assistant.
'''

class AIAdvisor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chat_history = []
        self.load_chat_history()
        self.setup_chain()
        # Add forecasting and anomaly detection tools
        from components.forecasting import FinancialForecaster
        from components.anomaly import AnomalyDetector
        self.forecaster = FinancialForecaster()
        self.anomaly_detector = AnomalyDetector()
    
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
        """Load chat history from file, ignore errors and don't show warnings to user"""
        chat_file = Path("data/chat_history/chat.json")
        if chat_file.exists():
            try:
                with open(chat_file, 'r') as f:
                    self.chat_history = json.load(f)
            except Exception as e:
                # Log error silently, don't show warning
                self.logger.error(f"Could not load chat history: {str(e)}")
                self.chat_history = []
    
    def save_chat_history(self):
        """Save chat history to file, convert non-serializable objects and suppress warnings"""
        chat_file = Path("data/chat_history/chat.json")
        try:
            # Convert DataFrames to dict or string summary before saving
            serializable_history = []
            for msg in self.chat_history:
                msg_copy = msg.copy()
                content = msg_copy.get("content")
                if isinstance(content, dict):
                    # If tool output contains DataFrame, convert to dict or summary
                    if "anomalies" in content and hasattr(content["anomalies"], "to_dict"):
                        anomalies = content["anomalies"]
                        msg_copy["content"] = dict(content)
                        msg_copy["content"]["anomalies"] = anomalies.head(10).to_dict()  # Only save first 10 rows
                    elif "forecast" in content and isinstance(content["forecast"], dict):
                        forecast = content["forecast"].copy()
                        if "data" in forecast and hasattr(forecast["data"], "to_dict"):
                            forecast["data"] = forecast["data"].head(10).to_dict()  # Only save first 10 rows
                        if "plot" in forecast:
                            forecast["plot"] = "[plot omitted]"
                        msg_copy["content"]["forecast"] = forecast
                serializable_history.append(msg_copy)
            with open(chat_file, 'w') as f:
                json.dump(serializable_history, f)
        except Exception as e:
            # Log error silently, don't show warning
            self.logger.error(f"Could not save chat history: {str(e)}")
    
    def parse_intent(self, input_text):
        """Parse user input to determine if it's a forecast, anomaly, or general query"""
        forecast_keywords = ["forecast", "predict", "future", "trend"]
        anomaly_keywords = ["anomaly", "anomalies", "unusual", "suspicious", "outlier", "detect"]
        text = input_text.lower()
        if any(word in text for word in forecast_keywords):
            return "forecast"
        if any(word in text for word in anomaly_keywords):
            return "anomaly"
        return "general"
    
    def generate_response(self, input_text, username=None):
        """Generate response using the financial advisor chain or run tools if needed"""
        # Add personalization if username is provided
        if username:
            input_text = f"User {username} asks: {input_text}"
        # Check for data
        data = None
        if 'current_data' in st.session_state and st.session_state.current_data is not None:
            data = st.session_state.current_data
        intent = self.parse_intent(input_text)
        if intent == "forecast" and data is not None:
            periods = 30  # default
            forecast_result = self.forecaster.generate_forecast(data, periods)
            # Prepare summary prompt for LLM
            summary_prompt = f"Summarize these forecast results for the user in a clear, actionable way: {forecast_result['metrics']}"
            summary = self.chain.invoke({"input": summary_prompt})
            return {"type": "forecast", "response": summary, "forecast": forecast_result}
        elif intent == "anomaly" and data is not None:
            anomalies = self.anomaly_detector.detect(data)
            # Prepare summary prompt for LLM
            if anomalies is not None and not anomalies.empty:
                summary_prompt = f"Summarize these anomaly results for the user in a clear, actionable way: {anomalies.describe(include='all').to_dict()}"
            else:
                summary_prompt = "No anomalies were detected in the data. Summarize this for the user."
            summary = self.chain.invoke({"input": summary_prompt})
            return {"type": "anomaly", "response": summary, "anomalies": anomalies}
        else:
            response = self.chain.invoke({"input": input_text})
            return {"type": "general", "response": response}
    
    def render(self):
        """Render the financial advisor interface"""
        st.subheader("Financial Chatbot & Advisor")
        with st.expander("How to use this chatbot", expanded=True):
            st.markdown("""
            - Ask any financial question.
            - To get a forecast, use words like 'forecast', 'predict', or 'future'.
            - To detect anomalies, use words like 'anomaly', 'unusual', or 'suspicious'.
            """)
        username = st.text_input("Enter your name for personalized advice", "")
        for message in self.chat_history:
            with st.chat_message(message["role"]):
                if isinstance(message["content"], dict):
                    # Tool result
                    if message["content"]["type"] == "forecast":
                        st.write(message["content"]["response"])
                        if "forecast" in message["content"] and "plot" in message["content"]["forecast"]:
                            st.plotly_chart(message["content"]["forecast"]["plot"], use_container_width=True)
                        if "forecast" in message["content"] and "data" in message["content"]["forecast"]:
                            st.dataframe(message["content"]["forecast"]["data"])
                    elif message["content"]["type"] == "anomaly":
                        st.write(message["content"]["response"])
                        anomalies = message["content"].get("anomalies")
                        if anomalies is not None and not anomalies.empty:
                            st.dataframe(anomalies)
                        else:
                            st.info("No anomalies detected.")
                    else:
                        st.write(message["content"]["response"])
                else:
                    st.write(message["content"])
        if prompt := st.chat_input("Ask a financial question, or request a forecast/anomaly detection"):
            self.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                result = self.generate_response(prompt, username)
                if isinstance(result, dict):
                    st.write(result["response"])
                    if result["type"] == "forecast" and "forecast" in result and "plot" in result["forecast"]:
                        st.plotly_chart(result["forecast"]["plot"], use_container_width=True)
                        st.dataframe(result["forecast"]["data"])
                    elif result["type"] == "anomaly":
                        anomalies = result.get("anomalies")
                        if anomalies is not None and not anomalies.empty:
                            st.dataframe(anomalies)
                        else:
                            st.info("No anomalies detected.")
                else:
                    st.write(result)
                self.chat_history.append({"role": "assistant", "content": result})
            self.save_chat_history()
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

