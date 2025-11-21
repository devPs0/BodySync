import requests

s = requests.Session()
# Attempt to login as 'dev' using known test credentials; adjust if needed
login = s.post('http://127.0.0.1:5000/login', data={'username':'dev','password':'dev'})
print('Login status', login.status_code)
resp = s.get('http://127.0.0.1:5000/get_progress')
print('Progress status', resp.status_code)
print(resp.text)
