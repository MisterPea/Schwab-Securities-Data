import urllib
from process_brokerage_data.account_methods import AccountMethods
from urllib.parse import quote
import requests
import datetime
import json
from process_brokerage_data.securities_data_types import (PriceHistoryOptions, IndexSymbolType, MoverSortType,
                                                          MoversFreqType,
                                                          MarketTimeType)


class SecuritiesData:
    def __init__(self):
        self.data_url = "https://api.schwabapi.com/marketdata/v1"
        self.account = AccountMethods()

    @staticmethod
    def convert_to_ms_epoch(yyyy_mm_dd: str):
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

    def price_history(self, symbol: str, price_history_options: PriceHistoryOptions):
        """Method to retrieve the price history of a specific instrument"""
        # Required params
        frequencyType = price_history_options.get('frequencyType')
        frequency = price_history_options.get('frequency')
        extendedHours = price_history_options.get('extendedHours')
        needPreviousClose = price_history_options.get('needPreviousClose')

        # Optional params
        startDate = price_history_options.get('startDate')
        endDate = price_history_options.get('endDate')
        periodType = price_history_options.get('periodType')
        period = price_history_options.get('period')

        # Check if dates provided
        date_params_provided = startDate is not None and endDate is not None

        # Check if periods provided
        period_params_provided = periodType is not None and period is not None

        # Check that either periods or dates provided - not both
        if period_params_provided == date_params_provided:
            raise ValueError(
                "You must provide either 'periodType' and 'period', "
                "or 'startDate' and 'endDate', but not both."
            )

        # Check for required params
        if symbol is None or frequencyType is None or frequency is None or extendedHours is None or needPreviousClose is None:
            raise ValueError("You must provide a 'symbol', 'frequencyType', 'frequency', extendedHours, and needPreviousClose.")

        symbol_list = [f"symbol={symbol}"]
        options_list = [f"{k}={v}" for [k, v] in price_history_options.items() if k not in ('startDate', 'endDate')]
        joined_options = "&".join(symbol_list + options_list)

        if startDate:
            joined_options += f"&startDate={self.convert_to_ms_epoch(startDate)}"
        if endDate:
            joined_options += f"&endDate={self.convert_to_ms_epoch(endDate)}"

        url = f"{self.data_url}/pricehistory?{joined_options}"
        print(url)
        headers = self.create_header()
        response = requests.get(url, headers=headers)

        # Check for success
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching price history: {response.status_code}, {response.text}")
            return None

    def get_movers(self, symbol: IndexSymbolType, sort_by: MoverSortType, freq: MoversFreqType):
        """This method should find the movers for the index symbol, but doesn't seem to work-This is a Schwab issue"""
        url = f"{self.data_url}/movers/{urllib.parse.quote(symbol)}?sort={sort_by}&frequency={urllib.parse.quote(f"{freq}")}"
        headers = self.create_header()

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching movers: {response.status_code}, {response.text}")
            return None

    def get_market_hours(self, market: MarketTimeType, date: str | None):
        url = f"{self.data_url}/markets/{market}{f"?date={date}" if date else ""}"
        headers = self.create_header()

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching market hours: {response.status_code}, {response.text}")
