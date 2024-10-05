from account_methods import AccountMethods
from typing import Literal, TypedDict
from urllib.parse import quote
import json
import requests
import datetime

PeriodType = Literal['day', 'month', 'year', 'ytd']
FrequencyType = Literal['minute', 'daily', 'weekly', 'monthly']

DayPeriod = Literal[1, 2, 3, 4, 5, 10]
MonthPeriod = Literal[1, 2, 3, 6]
YearPeriod = Literal[1, 2, 3, 5, 10, 15, 20]
YtdPeriod = Literal[1]
Period = DayPeriod | MonthPeriod | YearPeriod | YtdPeriod

MinuteFrequency = Literal[1, 5, 10, 15, 30]
OtherFrequency = Literal[1]

Frequency = MinuteFrequency | OtherFrequency  

class PriceHistoryOptions(TypedDict):
    period_type: PeriodType
    period: Period
    frequency_type: FrequencyType
    frequency: Frequency
    extended_hours: bool
    need_previous_close: bool
    start_date:str
    end_date: str

class SecuritiesData:
    def __init__(self):
        self.data_url = "https://api.schwabapi.com/marketdata/v1"
        self.account = AccountMethods()

    def convert_to_ms_epoch(self, yyyy_mm_dd:str):
        """Converts a date string in YYYY-MM-DD format to milliseconds since the epoch."""
        date_object = datetime.datetime.strptime(yyyy_mm_dd, "%Y-%m-%d")
        ms_epoch = int(date_object.timestamp() * 1000)
        return ms_epoch

    def create_header(self):
        """Method to prepare header with valid token"""
        token = self.account.get_token()
        headers = {
            "accept": "application/json",
            "Authorization": f'Bearer {token["access_token"]}',
        }
        return headers

    def get_quotes(self, symbols: list[str]):
        """Method to retrieve multiple quotes"""
        url = f"{self.data_url}/quotes?symbols={"".join([quote(s) for s in symbols])}&fields=quote&2Cfundamental&indicative=false"
        headers = self.create_header()
        response = requests.get(url, headers=headers)

        # Check for success
        if response.status_code == 200:
          return response.json()
        else:
          print(f"Error fetching market data: {response.status_code}, {response.text}")
          return None

    def price_history(self, symbol: str, options:PriceHistoryOptions):
        """Method to retrieve the price history of a specific instrument"""
        period_type = options.get('period_type','ytd')
        period=options.get('period',1)
        frequency_type=options.get('frequency_type','daily')
        frequency=options.get('frequency',1)
        needExtendedHoursData = options.get('extended_hours', False)
        needPreviousClose = options.get('need_previous_close', True)

        # Correct the list of strings for joining
        joined_options = "&".join([
            f"symbol={symbol}",
            f"periodType={period_type}",
            f"period={period}",
            f"frequencyType={frequency_type}",
            f"frequency={frequency}",
            f"needExtendedHoursData={needExtendedHoursData}",
            f"needPreviousClose={needPreviousClose}"
        ])

        url = f"{self.data_url}/pricehistory?{joined_options}"
        headers = self.create_header()
        response = requests.get(url, headers=headers)

        # Check for success
        if response.status_code == 200:
          return response.json()
        else:
          print(f"Error fetching price history: {response.status_code}, {response.text}")
          return None
        





options:PriceHistoryOptions={
   'period_type':"ytd",
   "period":1,
   "frequency_type":"daily",
   "frequency":1,
   "extended_hours":False,
   "need_previous_close":True
}

spy_out = SecuritiesData().price_history("SPY",options=options)
print(json.dumps(spy_out, indent=2))

