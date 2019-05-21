import requests

url = "https://github.com/123Mrxiao/hello-world/new/master"
response = requests.get(url)
print(response.text)
