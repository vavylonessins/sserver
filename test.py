import requests, json

response = requests.post("http://localhost:30795/api/test_scope/helloworld_func?a=1&b=2&c=3&s=ha%20ha%20ha")

if response.ok:
    print(json.loads(response.text))
else:
    print(response.text)

