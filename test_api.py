import requests
import json

# Test data
test_json = '{"name":"John","age":30,"city":"New York"}'

try:
    # Test format API
    response = requests.post('http://127.0.0.1:5000/api/format', 
                           json={'json_string': test_json, 'indent': 2})
    print("Format API Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test minify API
    response = requests.post('http://127.0.0.1:5000/api/minify', 
                           json={'json_string': test_json})
    print("Minify API Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")  
    print()
    
    # Test validate API
    response = requests.post('http://127.0.0.1:5000/api/validate', 
                           json={'json_string': test_json})
    print("Validate API Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to Flask app. Make sure it's running on http://127.0.0.1:5000")
except Exception as e:
    print(f"Error: {e}")
