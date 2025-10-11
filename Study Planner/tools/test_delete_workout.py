import requests

s = requests.Session()
# Try to login - update credentials if different
login_data = {'username': 'dev', 'password': 'devps0123'}
print('Logging in...')
r = s.post('http://127.0.0.1:5000/login', data=login_data)
print('Login status:', r.status_code)
print('Login text:', r.text[:200])

print('Calling delete_workout...')
r2 = s.post('http://127.0.0.1:5000/delete_workout', json={'index': 0})
print('Delete status:', r2.status_code)
print('Delete json:', r2.json())
