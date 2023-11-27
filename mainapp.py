import json
import datetime as dt
import requests
from matplotlib import pyplot as plt



## one asset info Function
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


## API KEY
api_key = '9wmIvPlT509xqeugo1MnzGIUubRlDRma'

## User input
asset_type = input(
    "what is the asset type you looking for?\nreturn  :stock / options / Indices / forex / crypto\nyour pick  - ").strip().lower()
symbol = input("Enter the requested asset symbol: ").upper()
##
if asset_type == 'options':
    symbol = 'O:' + symbol
elif asset_type == 'Indices':
    symbol = 'I:' + symbol
elif asset_type == 'forex':
    symbol = 'C:' + symbol
elif asset_type == 'crypto':
    symbol = 'X:' + symbol
else:
    symbol = symbol

## Calling one asset info function
get_your_asset_price = financial_asset_info(symbol, api_key)
## Response
print(f"""The last traded period info for {symbol} is:\n
Closing Price: {get_your_asset_price[0]}\nOpening Price: {get_your_asset_price[1]}\n
High Price: {get_your_asset_price[2]}\nLow Price: {get_your_asset_price[3]}\n
Volume: {get_your_asset_price[4]}\nNumber of Transactions: {get_your_asset_price[5]}\nVolume Weighted Average Price: {get_your_asset_price[6]}""")

## Chart option yes/no
chart_on_off = input("would you like to see a chart of the asset you picked ? (yes/no):  ").strip().lower()

if chart_on_off == "yes":
    from_date = input("starting date : (use the format yyyy-mm-dd hh:mm )-  ")
    to_date = input("ending date : (use the format yyyy-mm-dd hh:mm )-  ")
    time_frame = input("The size of the time window : (use the time frames like - day , minute , hour)").strip().lower()
    multiplier = int(input("The size of the time frame multiplier:  (use numbers only)"))
    limit_num_of_candels = int(input("Limits the number of base aggregates queried to create the aggregate results: "))

    chart_url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{time_frame}/{from_date}/{to_date}?adjusted=true&sort=desc&limit={limit_num_of_candels}&apiKey={api_key}"
    chart_response = requests.get(chart_url)
    chart = chart_response.json()

    if 'results' in chart and len(chart['results']) > 0:
        dates = [dt.datetime.fromtimestamp(item['t'] / 1000).strftime('%Y-%m-%d %H:%M') for item in chart['results']]
        prices = [item['c'] for item in chart['results']]
        # Plotting the data
        plt.figure(figsize=(10, 6))
        plt.plot(dates, prices, marker='o')
        plt.title(f'Prices Over Time for {symbol}, {multiplier} {time_frame} Aggregates Bars ')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.tight_layout()
        plt.show()
    else:
        print()
        print("No chart data available for this symbol.")
else:
    print()
    print("Ok, chart is not needed.")
print()


def financial_assets_list_info(symbol, api_key, start_date, end_date, time_frame, multiplier):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{time_frame}/{start_date}/{end_date}?unadjusted=true&apiKey={api_key}"

    response = requests.get(url)
    asset_data = response.json()
    if 'results' in asset_data and len(asset_data['results']) > 0:
        # Return a list of dictionaries, each containing 'date' and 'price'
        return [{'date': dt.datetime.fromtimestamp(item['t'] / 1000).strftime('%Y-%m-%d %H:%M'), 'price': item['c']} for
                item in asset_data['results']]
    else:
        return []


assets_comparison_on_chart = input("would you like to compare a list of assets? (yes/no): ").strip().lower()

## multiple assets on a single chart for comparison
if assets_comparison_on_chart == "yes":
    symbols_input = input("Enter a list of symbols for comparison (e.g., baba,msft,...): ").strip().upper()
    symbols_list = symbols_input.split(',')
    start_date = input("Starting date (use the format yyyy-mm-dd hh:mm): ")
    end_date = input("Ending date (use the format yyyy-mm-dd hh:mm): ")
    time_frame = input("The size of the time window (e.g., day, minute, hour): ").strip().lower()
    multiplier = int(input("The size of the time frame multiplier (use numbers only): "))

    assets_data = {}
    for symbol in symbols_list:
        assets_data[symbol] = financial_assets_list_info(symbol, api_key, start_date, end_date, time_frame, multiplier)

    # Plot data for each asset
    plt.figure(figsize=(12, 6))
    for symbol in symbols_list:
        if assets_data[symbol]:
            dates = [data_point['date'] for data_point in assets_data[symbol]]
            prices = [data_point['price'] for data_point in assets_data[symbol]]
            plt.plot(dates, prices, label=symbol)

    plt.title("Assets Price Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()
else:
    print("Ok, multi chart is not needed.")


