import streamlit as st
from streamlit_chat import message as st_message

# Function to simulate chatbot responses
def chatbot_response(user_input):
    # Here, you can integrate with an actual chatbot API or use simple rules
    if user_input.lower() in ["hi", "hello"]:
        return "Hello! How can I assist you today?"
    elif user_input.lower() in ["help", "features"]:
        return "I can help you with currency optimization, stock monitoring, and alerts for currency fluctuations."
    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"

st.title("Deutsche Bank Market Risks Analyser")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a feature:", ["Currency Optimizer", "Stock Monitor and Anomaly Detection", "Alerts for Currency Fluctuation"])

if page == "Currency Optimizer":
    # Import and run your currency optimizer script
    import app_currency  # Replace with your actual filename without .py
    app_currency.run()  # Ensure your currency optimizer script has a run() function

elif page == "Stock Monitor and Anomaly Detection":
    # Import and run your stock monitor script
    import Stock_Dashboard  # Replace with your actual filename without .py
    Stock_Dashboard.run()  # Ensure your stock monitor script has a run() function

else:
    # Import and run your currency optimizer script
    import alert_system  # Replace with your actual filename without .py
    alert_system.run()  # Ensure your alert system script has a run() function

# Chatbot Interface
st.sidebar.title("Chatbot")
user_input = st.sidebar.text_input("Type your question here:")
if user_input:
    response = chatbot_response(user_input)
    st_message(response, key="chatbot")
