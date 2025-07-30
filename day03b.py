import requests

# Example data to send to the server (replace with your actual input)
data = {
    'temperature': 1.0,
    'exhaust_vacuum': 2.0,
    'ambient_pressure': 3.0,
    'relative_humidity': 4.0
}

response = requests.post('http://127.0.0.1:5000/', json=data)

# Print the full server response
print('Full server response:', response.text)

# Handle the return value from the server
try:
    # Try to parse as float or list of floats if possible
    result = response.text.strip()
    # Remove all brackets
    result = result.replace('[', '').replace(']', '')
    # Split by comma in case of multiple values, take the first
    result = result.split(',')[0].strip()
    result_value = float(result)
    print('Predicted value from server:', result_value)
except Exception as e:
    print('Error parsing response:', e)
