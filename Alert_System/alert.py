import requests
import logging
from flask import Flask, request, jsonify
from twilio.rest import Client
from uagents import Agent, Context
import threading
import time

# Set up Flask
app = Flask(__name__)

# Set the logging level for the twilio.http_client logger to a higher level (e.g., WARNING)
logging.getLogger('twilio.http_client').setLevel(logging.WARNING)

# Store currency pairs and thresholds
currency_pairs = []
rate_check_interval = 60  # Default rate check interval in seconds

# Function to fetch the exchange rate
def get_exchange_rate(base_currency, target_currency):
    response = requests.get(f'https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/{base_currency}')
    data = response.json()
    conversion_rates = data.get('conversion_rates', {})
    exchange_rate = conversion_rates.get(target_currency)
    return exchange_rate

# Function to set up Twilio account credentials
def setup_twilio():
    account_sid = "YOUR_TWILIO_ACCOUNT_SID"
    auth_token = "YOUR_TWILIO_AUTH_TOKEN"
    twilio_phone_number = "+16789712415"  # Use your valid Twilio phone number here
    client = Client(account_sid, auth_token)
    return client, twilio_phone_number

# Function to send SMS using Twilio
def send_twilio_alert(message, client, twilio_phone_number):
    try:
        client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to="+917060297979"  # Replace with the phone number you want to send the alert to
        )
        print("Twilio alert sent successfully.")
    except Exception as e:
        print(f"Error sending Twilio alert: {str(e)}")

# Function to check exchange rates and send alerts
def check_exchange_rates(ctx):
    client, twilio_phone_number = setup_twilio()
    while True:
        for base, target, upper, lower in currency_pairs:
            exchange_rate = get_exchange_rate(base, target)
            if exchange_rate is not None:
                message = f'Current rate of 1 {base} is {exchange_rate} {target}'
                ctx.logger.info(message)

                if exchange_rate > upper:
                    alert_message = f'Alert: {base} to {target} rate is above {upper}'
                    ctx.logger.info(alert_message)
                    send_twilio_alert(alert_message, client, twilio_phone_number)

                elif exchange_rate < lower:
                    alert_message = f'Alert: {base} to {target} rate is below {lower}'
                    ctx.logger.info(alert_message)
                    send_twilio_alert(alert_message, client, twilio_phone_number)

        time.sleep(rate_check_interval)  # Wait for the defined interval before checking again

@app.route('/add_pair', methods=['POST'])
def add_currency_pair():
    data = request.json
    base_currency = data.get('base_currency', 'USD').upper()
    target_currency = data.get('target_currency', 'EUR').upper()
    upper_threshold = data.get('upper_threshold', 0)
    lower_threshold = data.get('lower_threshold', 0)

    # Check if the currency pair already exists in the list
    if (base_currency, target_currency) in [(pair[0], pair[1]) for pair in currency_pairs]:
        return jsonify({'message': f'The currency pair {base_currency} to {target_currency} is already in the list.'}), 400

    currency_pairs.append((base_currency, target_currency, upper_threshold, lower_threshold))
    return jsonify({'message': f'Currency pair {base_currency} to {target_currency} added successfully.'}), 200

@app.route('/check', methods=['POST'])
def check_currency():
    # This can still be called to check the current status
    # This endpoint could be useful to get the latest rates on demand
    return jsonify({'message': 'Currency check completed.'}), 200

if __name__ == '__main__':
    # Integration with uagents
    alice = Agent(name="Alice", seed="Alice recovery phrase")

    # Start the exchange rate checker in a separate thread
    @alice.on_interval(period=rate_check_interval)
    async def check_thresholds_wrapper(ctx: Context):
        check_exchange_rates(ctx)

    checker_thread = threading.Thread(target=alice.run)
    checker_thread.daemon = True  # Daemonize thread
    checker_thread.start()

    app.run(host='0.0.0.0', port=8000)  # Render expects apps to listen on port 8000
