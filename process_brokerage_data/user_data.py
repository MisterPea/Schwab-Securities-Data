import requests
from process_brokerage_data.account_methods import AccountMethods


class UserData:
    def __init__(self):
        self.user_data_url = "https://api.schwabapi.com/trader/v1"
        self.account = AccountMethods()

    def create_header(self):
        """Method to prepare header with valid token"""
        token = self.account.get_token()
        headers = {
            "accept": "application/json",
            "Authorization": f'Bearer {token["access_token"]}',
        }
        return headers

    def get_user_prefs(self):
        """Method to get user preferences"""
        url = f"{self.user_data_url}/userPreference"
        headers = self.create_header()
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching user preferences: {response.status_code}")
            return None
