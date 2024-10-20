import streamlit as st
import requests
import logging
from twilio.rest import Client
import threading
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

# Store currency pairs and thresholds
currency_pairs = []
rate_check_interval = 60  # Default rate check interval in seconds
stop_checking = False

# Function to fetch the exchange rate
def get_exchange_rate(base_currency, target_currency):
    response = requests.get(f'https://v6.exchangerate-api.com/v6/0f4cf71ee4a1546a11a36982/latest/USD')
    data = response.json()
    conversion_rates = data.get('conversion_rates', {})
    exchange_rate = conversion_rates.get(target_currency)
    return exchange_rate

# Function to set up Twilio account credentials
def setup_twilio():
    account_sid = "AC6d62829bb698a0219762ec06a64c827e"
    auth_token = "e72078234babc83ca50e96b78e0bbf35"
    twilio_phone_number = "+16789712415"  # Your Twilio phone number
    client = Client(account_sid, auth_token)
    return client, twilio_phone_number

# Function to send SMS using Twilio
def send_twilio_alert(message, client, twilio_phone_number):
    try:
        client.messages.create(
            body=message,
            from_="+16789712415",
            to="+917060297979"  # Replace with the phone number you want to send the alert to
        )
        logging.info("Twilio alert sent successfully.")
    except Exception as e:
        logging.error(f"Error sending Twilio alert: {str(e)}")

# Function to check exchange rates and send alerts
def check_exchange_rates():
    client, twilio_phone_number = setup_twilio()
    while not stop_checking:
        for base, target, upper, lower in currency_pairs:
            exchange_rate = get_exchange_rate(base, target)
            if exchange_rate is not None:
                message = f'Current rate of 1 {base} is {exchange_rate} {target}'
                logging.info(message)

                if exchange_rate > upper:
                    alert_message = f'Alert: {base} to {target} rate is above {upper}'
                    logging.info(alert_message)
                    send_twilio_alert(alert_message, client, twilio_phone_number)

                elif exchange_rate < lower:
                    alert_message = f'Alert: {base} to {target} rate is below {lower}'
                    logging.info(alert_message)
                    send_twilio_alert(alert_message, client, twilio_phone_number)

        time.sleep(rate_check_interval)

# Run function for the alert system
def run():
    global stop_checking, currency_pairs

    st.header("Alerts for Currency Fluctuation")
    base_currency = st.text_input("Base Currency (e.g., USD)", "USD").upper()
    target_currency = st.text_input("Target Currency (e.g., EUR)", "EUR").upper()
    upper_threshold = st.number_input("Upper Threshold", value=0.0)
    lower_threshold = st.number_input("Lower Threshold", value=0.0)

    if st.button("Add Currency Pair"):
        currency_pairs.append((base_currency, target_currency, upper_threshold, lower_threshold))
        st.success(f"Currency pair {base_currency} to {target_currency} added successfully!")

    if st.button("Start Monitoring"):
        stop_checking = False
        checker_thread = threading.Thread(target=check_exchange_rates)
        checker_thread.daemon = True  # Daemonize thread
        checker_thread.start()
        st.success("Started monitoring currency pairs!")

    if st.button("Stop Monitoring"):
        stop_checking = True
        st.success("Stopped monitoring currency pairs!")

    # Display the current currency pairs being monitored
    st.write("Monitoring the following currency pairs:")
    for pair in currency_pairs:
        st.write(f"{pair[0]} to {pair[1]}: Upper Threshold = {pair[2]}, Lower Threshold = {pair[3]}")

# Entry point for the application
if __name__ == "__main__":
    run()
