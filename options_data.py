import urllib
from dataclasses import asdict
from urllib.parse import quote
from account_methods import AccountMethods
import json
import requests
import datetime
from option_data_types import OptionExpirationType, OptionChainRequest, OptionReturnType


class OptionData:
    def __init__(self):
        self.data_url = "https://api.schwabapi.com/marketdata/v1"
        self.account = AccountMethods()

    def create_header(self):
        """Method to prepare header with valid token"""
        token = self.account.get_token()
        headers = {
            "accept": "application/json",
            "Authorization": f'Bearer {token["access_token"]}',
        }
        return headers

    @staticmethod
    def print_output(json_data: dict):
        print(json.dumps(json_data, indent=2))

    def get_expiration_chain(self, symbol: str) -> OptionExpirationType | None:
        """Retrieves the expiration chain for the options of a given symbol."""
        url = f"{self.data_url}/expirationchain?symbol={symbol}"
        headers = self.create_header()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching expiration chain for {symbol}")
            return None

    def get_option_chain(self, chain_options: OptionChainRequest) -> OptionReturnType | None:
        headers = self.create_header()
        url_options = ""
        chain_options_dict = asdict(chain_options)
        url_parts = []
        for key, value in chain_options_dict.items():
            if value:
                if type(value) == bool:
                    value = "true" if value else "false"
                url_parts.append(f"{key}={value}")
        print("&".join(url_parts))
        url = f"{self.data_url}/chains?{"&".join(url_parts)}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching option chain for {chain_options.symbol}")
            return None
