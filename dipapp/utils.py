
import requests
import pycountry
def get_currency_symbol(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country:
            currency = pycountry.currencies.get(alpha_3=country.alpha_3)
            if currency:
                return currency.symbol
    except Exception as e:
        print(f"Error getting currency symbol: {e}")
    return '$'  # Default to '$' if not found

def get_user_country(request):
    ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
    print(ip)
    response = requests.get(f'https://ipinfo.io/{ip}/json')
    data = response.json()
    print(data)
    return data.get('country', 'US')  # Default to US if the country is not available
