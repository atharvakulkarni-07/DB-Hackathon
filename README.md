# Deutsche Bank Market Risks Analyser 📊

## Overview

The **Deutsche Bank Market Risks Analyser** is a comprehensive web application built with **Streamlit** that provides tools for monitoring currency rates, analyzing stock market data, and managing alerts for currency fluctuations. This application is designed for users who want to gain insights into market trends and make informed financial decisions.

## Features

### 1. Currency Optimizer 💱
- **Real-Time Monitoring**: Keep track of live currency exchange rates for various currency pairs, helping users stay informed about market fluctuations.
- **Threshold Setting**: Users can set upper and lower thresholds for specific currency pairs to define their desired exchange rate limits.
- **SMS Alerts**: Leverage the **Twilio API** to receive SMS notifications when currency rates exceed specified thresholds, ensuring users never miss important market movements.

### 2. Stock Monitor and Anomaly Detection 📈
- **Stock Data Analysis**: Analyze comprehensive stock market data to understand trends and make data-driven investment decisions.
- **Visual Performance Insights**: Visualize stock performance over time with interactive charts, making it easier to identify historical trends and future predictions.
- **Anomaly Detection**: Identify unusual patterns in stock price movements using advanced analytics techniques, alerting users to potential investment opportunities or risks.

### 3. Alerts for Currency Fluctuation 🔔
- **Customizable Alerts**: Set up personalized alerts based on currency fluctuations that matter most to the user.
- **Notifications**: Receive timely notifications when specific conditions are met, keeping users informed and proactive about their financial strategies.
- **Flexible Monitoring Settings**: Customize monitoring settings to suit user preferences, ensuring an optimal user experience tailored to individual needs.

### 4. Chatbot Integration 🤖
- **Interactive Chatbot**: Engage with a chatbot powered by **OpenAI’s language model**, providing users with instant answers to their queries.
- **Real-Time Assistance**: Ask questions and receive insightful responses in real-time, enhancing the overall user experience.
- **Seamless UI Integration**: The chatbot is conveniently integrated into the UI for easy access, making it simple for users to get help whenever they need it.

## Technologies Used 🛠️

- **Frontend**: Streamlit for creating an interactive web interface.
- **Backend**: Python for the core application logic and data processing.
- **APIs**:
  - [ExchangeRate-API](https://www.exchangerate-api.com/) for accessing real-time currency exchange rates.
  - [Twilio API](https://www.twilio.com/) for sending SMS alerts to users.
  - [OpenAI API](https://openai.com/) for powering the chatbot.
- **Libraries**:
  - `requests`: For making API calls to external services.
  - `logging`: For error tracking and debugging.
  - `threading`: For implementing asynchronous monitoring of currency rates and alerts.

## Installation 🏗️

To run the application locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/market-risks-analyser.git
   cd market-risks-analyser
   

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
