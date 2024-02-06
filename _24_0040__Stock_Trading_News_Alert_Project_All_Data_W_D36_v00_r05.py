import requests, os, re
# import newsapi-python
from twilio.rest import Client
from datetime import datetime as dt
from datetime import timedelta


# TODO: Environment Variables to still apply:
# api_KEY  (for each API website):

STOCK_PRICE_API_KEY = os.environ.get('STOCK_PRICE_API_KEY')    #the API Key from the open weather website
print(f"The stock price api key is: {STOCK_PRICE_API_KEY}")

# news_api_key =
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')    #the API Key from the open weather website
print(f"The news price api key is: {NEWS_API_KEY}")
print()

# twilio_api_key =


#Normal Variables:
STOCK1 = "AMZN"
COMPANY_NAME = "Amazon.com, Inc."

# account_SID (for each API):


# auth_TOKEN (for each API):



# TODO: STEP 1: Use https://www.alphavantage.co
# When STOCK1 price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO: STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO: STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#------------------------- START OF STEP 1 -------------------------#
# Use https://www.alphavantage.co
# When STOCK1 price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# API_Weather_URL_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
full_stock_sample_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo"
Stock_Price_Alpha_Avan_URL_Endpoint = "https://www.alphavantage.co/query"

# Required Params:
'''
API Parameters
❚ Required: function

The time series of your choice. In this case, function=TIME_SERIES_INTRADAY

❚ Required: symbol

The name of the equity of your choice. For example: symbol=IBM

❚ Required: interval

Time interval between two consecutive json_data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min
'''

# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK1}&apikey={STOCK_PRICE_API_KEY}'
response = requests.get(stock_url)
response.raise_for_status()
json_data = response.json()
# print(json_data)

now = dt.now()
print(f"Now is: {now}")

# now_day = now.day
# print(f"now.day is: {now_day}")

# day_of_week = now.weekday()
# print(f"now.weekday is: {day_of_week}")

now_hour = now.hour
print(f"now.hour is: {now_hour}")
print()

def is_valid_date(date_str):
    # Regex to check if the date is in the format YYYY-MM-DD
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        try:
            # Check if it's a valid date
            dt.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            # String matches format but is not a valid date
            return False
    return False

# Assuming json_data is your JSON response from the API
time_series_daily = json_data.get('Time Series (Daily)', {})
dates = list(time_series_daily.keys())

if dates:
    first_date = dates[0]  # Get the first date
    print(f"The first date discovered is: {first_date}")
    if is_valid_date(first_date):
        first_date_obj = dt.strptime(first_date, '%Y-%m-%d')
        print(f"The first day object is: {first_date_obj}")
        day_of_the_week_for_first_day = (first_date_obj.strftime("%A"))   #converts it back into a string. No need to convert it manually.
        print(f"The day of the week of {first_date} is: {day_of_the_week_for_first_day}")
        first_date_data = time_series_daily[first_date]
        values = list(first_date_data.values())
        if len(values) >= 4:
            fourth_value_of_day_before = values[3]  # Get the fourth value
            print(f"The fourth value for {first_date} is: {fourth_value_of_day_before}")

stock_price_comparison1 = float(fourth_value_of_day_before)

# Assuming first_date is a string in 'YYYY-MM-DD' format:
first_date_str = first_date  # Example date
first_date_obj = dt.strptime(first_date_str, '%Y-%m-%d')

# Subtract one day:
one_day_before = first_date_obj - timedelta(days=1)

# Convert back to string if needed:
one_day_before_str = one_day_before.strftime('%Y-%m-%d')
print(f"The day before would be: {one_day_before_str}")

print()

if dates:
    print(f"The first date discovered is: {one_day_before_str}")
    if is_valid_date(one_day_before_str):
        one_day_before_obj = dt.strptime(one_day_before_str, '%Y-%m-%d')
        print(f"The first day object is: {one_day_before_obj}")
        day_of_the_week_for_first_day = (one_day_before_obj.strftime("%A"))   #converts it back into a string. No need to convert it manually.
        print(f"The day of the week of {one_day_before_str} is: {day_of_the_week_for_first_day}")
        one_day_before_data = time_series_daily[one_day_before_str]
        values = list(one_day_before_data.values())
        if len(values) >= 4:
            fourth_value_of_day_before = values[3]  # Get the fourth value
            print(f"The fourth value for {one_day_before_str} is: {fourth_value_of_day_before}")

stock_price_comparison2 = float(fourth_value_of_day_before)

absolute_difference_between_2_days = abs(float(stock_price_comparison1 / stock_price_comparison2))
ab_diff = ((absolute_difference_between_2_days-1) * 100)
print(f"The difference between {one_day_before_str} and {first_date_str} is: {ab_diff}")

if ab_diff >= 5.00:
    # TEXT THIS:
    print("Wow. That's a 5% change in one day!")

#------------------------- END OF STEP 1 -------------------------#

#------------------------- START OF STEP 2 -------------------------#
# Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_url = f"https://newsapi.org/v2/everything?q={STOCK1}&apiKey={NEWS_API_KEY}"
response2 = requests.get(news_url)
response2.raise_for_status()
news_json_data = response2.json()
# print(news_json_data)
print(news_json_data['articles'][0]['content'])
print(news_json_data['articles'][1]['content'])
print(news_json_data['articles'][2]['content'])


#------------------------- END OF STEP 2 -------------------------#

#------------------------- START OF STEP 3 -------------------------#
# Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.




#------------------------- END OF STEP 3 -------------------------#

#------------------------- START OF OPTIONAL STEP 4 -------------------------#
# TODO: STEP 4: Optional: Format the SMS message like this:

"""
AMZN: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Amazon.com, Inc. (AMZN)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"AMZN: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Amazon.com, Inc. (AMZN)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
