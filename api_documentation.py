# http client api
import http.client

conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "b601f35c12mshc29496541aa961dp15bad3jsn531508573071",
    'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
}

conn.request("GET", "/seasons", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

# requests api
import requests

url = "https://api-nba-v1.p.rapidapi.com/seasons"

headers = {
	"X-RapidAPI-Key": "b601f35c12mshc29496541aa961dp15bad3jsn531508573071",
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())