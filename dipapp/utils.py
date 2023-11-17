
import requests

def get_user_country(request):
    ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
    response = requests.get(f'https://ipinfo.io/{ip}/json')
    data = response.json()
    return data.get('country', 'US')  # Default to US if the country is not available
