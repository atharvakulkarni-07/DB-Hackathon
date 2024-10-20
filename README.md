# Stock Anomaly Detection with Bollinger Bands

This project is a **Gradio-based web application** that detects anomalies in stock prices using **Bollinger Bands**. It retrieves stock data from Yahoo Finance and uses technical indicators to visualize price trends and identify anomalies where the stock price breaks above or below the Bollinger Bands.

### Live Application

The application is live and can be accessed here:
[Stock Anomaly Detection with Bollinger Bands](https://db-hackathon-1.onrender.com)

## Features

- Retrieves the last 5 years of stock data from Yahoo Finance.
- Calculates Bollinger Bands based on a user-defined window size and number of standard deviations.
- Detects anomalies when the stock price crosses above or below the Bollinger Bands.
- Visualizes the stock price, Bollinger Bands, and anomalies using **Plotly** charts.
- User-friendly interface using **Gradio** where users can:
  - Select from a list of stock tickers.
  - Adjust the window size and standard deviations for Bollinger Band calculations.
  
## Technologies Used

- **Python**: Main programming language.
- **Gradio**: For building the interactive web interface.
- **Yahoo Finance API (via yfinance)**: For fetching stock data.
- **Plotly**: For data visualization and interactive charting.
- **Render**: For deploying the web application.

## How to Use

1. **Select a stock ticker** from the dropdown menu (e.g., AAPL, MSFT, GOOGL).
2. **Adjust the window size** for the Simple Moving Average (SMA) used in the Bollinger Bands calculation.
3. **Adjust the number of standard deviations** to widen or narrow the bands.
4. The chart will automatically update to display the stock price, Bollinger Bands, and any detected anomalies.

## Running Locally

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
