import streamlit as st
import json
import datetime as dt
import requests
import matplotlib.pyplot as plt

# One asset info Function
def financial_asset_info(symbol, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    asset_data = response.json()
    if 'results' in asset_data and len(asset_data['results']) > 0:
        closing_price = asset_data['results'][0]['c']
        opening_price = asset_data['results'][0]['o']
        high_price = asset_data['results'][0]['h']
        low_price = asset_data['results'][0]['l']
        traded_volume = asset_data['results'][0]['v']
        number_of_transactions = asset_data['results'][0]['n']
        VWAP = asset_data['results'][0]['vw']
        return closing_price, opening_price, high_price, low_price, traded_volume, number_of_transactions, VWAP
    else:
        return "No data available for this symbol."

# Fetching historical data for a list of assets
def financial_assets_list_info(symbol, api_key, start_date, end_date, time_frame, multiplier):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{time_frame}/{start_date}/{end_date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    asset_data = response.json()
    if 'results' in asset_data and len(asset_data['results']) > 0:
        return [{'date': dt.datetime.fromtimestamp(item['t'] / 1000).strftime('%Y-%m-%d %H:%M'), 'price': item['c']} for item in asset_data['results']]
    else:
        return []

# Streamlit app layout
st.title("Financial Asset Information and Comparison")

api_key = '9wmIvPlT509xqeugo1MnzGIUubRlDRma'
asset_type = st.selectbox("Select the asset type", ['stock', 'options', 'Indices', 'forex', 'crypto'])
symbol = st.text_input("Enter the requested asset symbol").upper()

if st.button("Get Asset Info"):
    get_your_asset_price = financial_asset_info(symbol, api_key)
    if get_your_asset_price != "No data available for this symbol.":
        st.write(f"The last traded period info for {symbol} is:")
        st.write(f"""
            - Closing Price: {get_your_asset_price[0]}
            - Opening Price: {get_your_asset_price[1]}
            - High Price: {get_your_asset_price[2]}
            - Low Price: {get_your_asset_price[3]}
            - Volume: {get_your_asset_price[4]}
            - Number of Transactions: {get_your_asset_price[5]}
            - Volume Weighted Average Price: {get_your_asset_price[6]}
        """)
    else:
        st.write("No data available for this symbol.")

if st.checkbox("Would you like to see a chart of the asset?"):
    from_date = st.date_input("Starting date")
    to_date = st.date_input("Ending date")
    time_frame = st.selectbox("Select the size of the time window", ['day', 'minute', 'hour'])
    multiplier = st.number_input("Enter the size of the time frame multiplier", min_value=1, value=1)
    limit_num_of_candles = st.number_input("Limit the number of base aggregates", min_value=1, value=100)

    chart_url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{time_frame}/{from_date}/{to_date}?adjusted=true&sort=desc&limit={limit_num_of_candles}&apiKey={api_key}"
    chart_response = requests.get(chart_url)
    chart = chart_response.json()

    if 'results' in chart and len(chart['results']) > 0:
        dates = [dt.datetime.fromtimestamp(item['t'] / 1000).strftime('%Y-%m-%d %H:%M') for item in chart['results']]
        prices = [item['c'] for item in chart['results']]
        plt.figure(figsize=(10, 6))
        plt.plot(dates, prices, marker='o')
        plt.title(f'Prices Over Time for {symbol}, {multiplier} {time_frame} Aggregates Bars ')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("No chart data available for this symbol.")

if st.checkbox("Would you like to compare a list of assets?"):
    symbols_input = st.text_input("Enter a list of symbols for comparison (e.g., baba, msft,...)").strip().upper()
    if symbols_input:
        symbols_list = symbols_input.split(',')
        start_date = st.date_input("Starting date for comparison")
        end_date = st.date_input("Ending date for comparison")
        time_frame = st.selectbox("Select the size of the time window for comparison", ['day', 'minute', 'hour'])
        multiplier = st.number_input("Enter the size of the time frame multiplier for comparison", min_value=1, value=1)

        assets_data = {}
        for symbol in symbols_list:
            assets_data[symbol] = financial_assets_list_info(symbol, api_key, start_date, end_date, time_frame, multiplier)

        # Plot data for each asset
        fig, ax = plt.subplots(figsize=(12, 6))
        for symbol in symbols_list:
            if assets_data[symbol]:
                dates = [data_point['date'] for data_point in assets_data[symbol]]
                prices = [data_point['price'] for data_point in assets_data[symbol]]
                ax.plot(dates, prices, label=symbol)

        ax.set_title("Assets Price Comparison")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        st.pyplot(fig)
