import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

def run():
    # Set the title of the app
    st.title("Live Stock Monitor with Anomaly Detection")

    # Define a dictionary of companies and their ticker symbols
    companies = {
        "Apple": "AAPL",
        "Google": "GOOGL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Tesla": "TSLA",
        "Meta": "META",
        "NVIDIA": "NVDA",
        "Netflix": "NFLX"
    }

    # Create a select box for company selection
    selected_company = st.selectbox("Select a Company:", list(companies.keys()))
    ticker = companies[selected_company]

    # Fetch the stock data
    stock_data = yf.Ticker(ticker)
    df = stock_data.history(period="1mo")

    # Display the latest data for the selected company
    st.write(f"## Latest data for {selected_company} ({ticker})")
    st.write(df)

    # Calculate min and max prices for dynamic scaling
    min_price = df['Close'].min()
    max_price = df['Close'].max()

    # Create an Altair chart with dynamic y-axis scaling
    chart = alt.Chart(df.reset_index()).mark_line().encode(
        x='Date:T',
        y=alt.Y('Close:Q', scale=alt.Scale(domain=[min_price - 10, max_price + 10])),
        tooltip=['Date:T', 'Close:Q']
    ).properties(
        width=700,
        height=400
    )

    # Render the chart in the Streamlit app
    st.altair_chart(chart, use_container_width=True)

    # Function to download stock data
    def download_stock_data(ticker):
        stock_data = yf.Ticker(ticker)
        df = stock_data.history(period="5y")[['Close']]
        return df

    # Function to calculate Bollinger Bands
    def calculate_bollinger_bands(df, window, no_of_stds):
        rolling_mean = df['Close'].rolling(window=window).mean()
        rolling_std = df['Close'].rolling(window=window).std()
        df['Bollinger High'] = rolling_mean + (rolling_std * no_of_stds)
        df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_stds)
        return df

    # Function to detect anomalies
    def detect_anomalies(df):
        anomalies = (df['Close'] > df['Bollinger High']) | (df['Close'] < df['Bollinger Low'])
        return anomalies

    # Function to plot anomalies
    def plot_anomalies(ticker, window, no_of_stds):
        df = download_stock_data(ticker)
        df_with_bands = calculate_bollinger_bands(df, window, no_of_stds)
        anomalies = detect_anomalies(df_with_bands)
        df_with_bands['Anomaly'] = anomalies

        # Record the most recent anomaly date and price
        recent_anomalies = df_with_bands[df_with_bands['Anomaly']]
        if not recent_anomalies.empty:
            recent_date = recent_anomalies.index[-1]  # Get the most recent anomaly date
            recent_price = recent_anomalies['Close'].iloc[-1]  # Get the price at that anomaly
            st.session_state['recent_anomaly'] = (recent_date, recent_price)  # Store in session state

        # Create the Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_with_bands.index, y=df_with_bands['Close'],
                                 mode='lines', name='Close Price'))
        fig.add_trace(go.Scatter(x=df_with_bands.index, y=df_with_bands['Bollinger High'],
                                 line=dict(width=1), name='Bollinger High'))
        fig.add_trace(go.Scatter(x=df_with_bands.index, y=df_with_bands['Bollinger Low'],
                                 line=dict(width=1), name='Bollinger Low'))
        fig.add_trace(go.Scatter(x=df_with_bands.index,
                                 y=df_with_bands['Close'].where(df_with_bands['Anomaly']),
                                 mode='markers', name='Anomaly', marker=dict(color='red', size=8)))

        fig.update_layout(title=f'Bollinger Bands and Anomalies for {ticker}',
                          xaxis_title='Date', yaxis_title='Price', height=600)
        return fig

    # Slider for SMA window size
    window_size = st.slider("Select Window Size for SMA:", min_value=5, max_value=50, value=20)

    # Slider for standard deviation
    num_std_dev = st.slider("Select Number of Standard Deviations:", min_value=1, max_value=5, value=2)

    # Button for anomaly detection
    if st.button("Identify Anomalies"):
        anomaly_fig = plot_anomalies(ticker, window_size, num_std_dev)
        
        # Display the anomaly plot
        st.plotly_chart(anomaly_fig)

        # Check if there is a recent anomaly stored
        if 'recent_anomaly' in st.session_state:
            anomaly_date, anomaly_price = st.session_state['recent_anomaly']
            st.write(f"Most Recent Anomaly Detected on: {anomaly_date.date()} with Price: ${anomaly_price:.2f}")

    # Checkbox for querying anomalies
    if st.checkbox("Ask about the recent anomaly"):
        if 'recent_anomaly' in st.session_state:
            anomaly_date, anomaly_price = st.session_state['recent_anomaly']
            st.write(f"Most recent anomaly was detected on: {anomaly_date.date()} with price: ${anomaly_price:.2f}.")
        else:
            st.write("No recent anomalies detected.")

# This line ensures the script runs when called directly
if __name__ == "__main__":
    run()