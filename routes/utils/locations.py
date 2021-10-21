import requests


def reverse_geo_location(obj, from_latlon=False, limit_results=10):
    API_KEY = '385e86a3fdbb531401ecdabc08f01131'  # TODO: STORE THIS AWAY!
    url = 'http://api.positionstack.com/v1'
    if from_latlon:
        latitude, longitude = obj.get('latitude'), obj.get('longitude')
        query = f'{latitude},{longitude}'
        endpoint = 'reverse'
    else:
        street, city, country = obj.get('street', ''), obj.get('city', ''), obj.get('country', '')
        query = f'{street}, {city} ,{country}'
        endpoint = 'forward'

    full_url = f"{url}/{endpoint}?access_key={API_KEY}&query={query}&limit={limit_results}"
    resp = requests.get(full_url)

    if resp.status_code == 200:
        return resp.json()
    return None
