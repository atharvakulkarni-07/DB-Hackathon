import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt

# Define the currency codes dictionary
countries_currency_codes = {
    'Bahrain': 'BHD', 'Egypt': 'EGP', 'Israel': 'ILS', 'Nigeria': 'NGN',
    'Qatar': 'QAR', 'Saudi Arabia': 'SAR', 'South Africa': 'ZAR', 'Turkey': 'TRY',
    'UAE': 'AED', 'Brazil': 'BRL', 'Canada': 'CAD', 'Mexico': 'MXN', 'USA': 'USD',
    'Australia': 'AUD', 'China': 'CNY', 'Japan': 'JPY', 'India': 'INR', 
    'United Kingdom': 'GBP', 'Germany': 'EUR', 'France': 'EUR', 'Poland': 'PLN'
}

def run():
    st.title("Currency Portfolio Optimizer")

    # Step 1: User input for reference currency
    reference_currency_name = st.selectbox(
        "Select a reference currency:",
        list(countries_currency_codes.keys())
    )
    n = st.slider("Number of least correlated currencies to include:", 1, 5, 2)

    if st.button("Optimize Portfolio"):
        # Fetch currency codes
        reference_currency_code = countries_currency_codes[reference_currency_name]

        # Step 2: Download currency data from Yahoo Finance
        currency_data = {}
        for name, code in countries_currency_codes.items():
            ticker = f'USD{code}=X'
            if ticker == 'USDUSD=X':
                currency_data[code] = pd.Series([1] * 500)  # Dummy data for USD/USD
            else:
                currency_data[code] = yf.download(ticker, start='2020-10-20', end='2024-10-15')['Close']

        ticker_ref = f'USD{reference_currency_code}=X'
        data_ref = yf.download(ticker_ref, start='2020-10-20', end='2024-10-15')['Close']

        # Step 3: Compute correlation with reference currency
        correlation_dict = {}
        for code, data in currency_data.items():
            correlation = data_ref.corr(data)
            correlation_dict[code] = correlation

        # Step 4: Identify least correlated currencies
        least_correlated = sorted(correlation_dict, key=correlation_dict.get)[:n]

        # Fetch selected currency data
        selected_currencies = [currency_data[code] for code in least_correlated]
        selected_currencies.insert(0, data_ref)
        currency_values = pd.concat(selected_currencies, axis=1).to_numpy()

        # Portfolio Optimization
        col_names = ['Currency_' + str(i + 1) for i in range(n + 1)]
        data = pd.DataFrame(currency_values, columns=col_names)
        returns = data.pct_change().dropna()

        # Compute expected returns and covariance matrix
        expected_returns = returns.mean()
        cov_matrix = returns.cov()

        def portfolio_variance(weights):
            return np.dot(weights.T, np.dot(cov_matrix, weights))

        # Constraints and bounds for optimization
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(len(expected_returns)))
        initial_guess = [1 / len(expected_returns)] * len(expected_returns)

        # Optimize portfolio weights
        optimal = sco.minimize(portfolio_variance, initial_guess, method='SLSQP', 
                               bounds=bounds, constraints=constraints)
        optimal_weights = optimal.x

        # Generate portfolio values
        val = 1000  # Initial investment value
        og = [val * data_ref.iloc[0] / data_ref.iloc[i] for i in range(len(data_ref))]
        better_og = []
        
        for i in range(len(data_ref)):
            new_value = optimal_weights[0] * val * data_ref.iloc[0] / data_ref.iloc[i]
            for j in range(n):
                new_value += optimal_weights[j + 1] * val * currency_data[least_correlated[j]].iloc[0] / \
                             currency_data[least_correlated[j]].iloc[i]
            better_og.append(new_value)

        # Step 5: Display results
        st.subheader("Portfolio Details")
        best_countries = [key for key, value in countries_currency_codes.items() if value in least_correlated]
        best_countries.insert(0, reference_currency_name)

        st.write("Optimal Weights:")
        st.dataframe(pd.DataFrame({
            'Currency': best_countries,
            'Weight (%)': np.round(optimal_weights * 100, 2)
        }))

        # Plot the portfolio performance
        plt.figure(figsize=(8, 5))
        plt.plot(data_ref.index, og, label=f'Value of {reference_currency_code} vs USD', color='blue')
        plt.plot(data_ref.index, better_og, label='Value of Optimized Portfolio', color='orange')
        plt.xlabel('Date')
        plt.ylabel('Value (in USD)')
        plt.title('Currency vs Portfolio Value Over Time')
        plt.legend()
        st.pyplot(plt)

        # Save the plot
        plt.savefig('Plot_of_portfolio_vs_reference_currency.png')

# This line ensures the script runs when called directly
if __name__ == "__main__":
    run()
