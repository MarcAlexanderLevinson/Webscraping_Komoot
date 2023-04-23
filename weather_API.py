import requests

city = "Lyon"
start_date = "2023-01-01"
end_date = "2023-01-31"
key = "534887c399c84ceaa49ed2e322168f29"

cool_features = ['wind_spd', 'temp', 'max_temp', 'min_temp', 'clouds', 'precip', 'snow_depth']

url = f"https://api.weatherbit.io/v2.0/history/daily?city={city}&start_date={start_date}&end_date={end_date}&key={key}"
r = requests.get(url)

data = r.json()

print(data)
print(data['data'][0])
print(data['data'][1])
print(data['data'][2])
print()
print(data['data'][2].keys())






