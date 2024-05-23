import requests

class ApiNba:
    def __init__(self):
        self.url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

        self.headers = {
            "X-RapidAPI-Key": "b601f35c12mshc29496541aa961dp15bad3jsn531508573071",
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }

    def lebron(self):
        self.querystring = {"id":"265","season":"2023"}
        self.response = requests.get(self.url, headers=self.headers, params=self.querystring)

        return self.response.json()
    
    def steph(self):
        self.querystring = {"id":"124","season":"2023"}
        self.response = requests.get(self.url, headers=self.headers, params=self.querystring)

        return self.response.json()
    
    def jokic(self):
        self.querystring = {"id":"279","season":"2023"}
        self.response = requests.get(self.url, headers=self.headers, params=self.querystring)

        return self.response.json()
