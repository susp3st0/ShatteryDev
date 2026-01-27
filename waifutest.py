import requests

url = "https://api.waifu.im/search"
params = {
    "included_tags[]": ["maid"]
}

r = requests.get(url, params=params)

if r.status_code == 200:
    data = r.json()
    print(data["images"][0]["url"])
else:
    print("Failed:", r.status_code, r.text)
