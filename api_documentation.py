import requests

url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

querystring = {"id":"265","season":"2023"}

headers = {
	"X-RapidAPI-Key": "b601f35c12mshc29496541aa961dp15bad3jsn531508573071",
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())