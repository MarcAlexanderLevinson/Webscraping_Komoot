import requests



url = "https://api.weatherbit.io/v2.0/history/daily?&city=RhoneAlpes&start_date=2023-04-16&end_date=2023-04-17&key=f06beec8ff0447ca80e6c6cfba8250af"

for i in range(1000):
r = requests.get(url)
print(r.text)
