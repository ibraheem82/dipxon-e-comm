import requests
import pycountry
import os
from dotenv import load_dotenv
from accounts.models import Customer
load_dotenv()
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist

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

    api_key = os.getenv('IPSTACK_API_KEY')  # Change to your ipstack API key
    if api_key is None:
        raise Exception('IPSTACK_API_KEY environment variable not set')

    ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
    print(f"Request: IP - {ip}")

    # Check if the IP address is 127.0.0.1
    if ip == '127.0.0.1':
        print("IP address is localhost. Returning Dollar. $")
        return 'US'  # Return 'US' for United State, which corresponds to Naira

    try:
        response = requests.get(f'http://api.ipstack.com/{ip}?access_key={api_key}')
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        print(data)

        # Extract the country code from the response
        country_code = data.get('country_code')

        if country_code is None:
            # Handle the case where country information is not available
            print("Country information not available.")
            return 'US'  # Return 'US' for United State, which corresponds to dollar

        return country_code  # Return the country code, not the entire dictionary

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

    # If an error occurred, return a default value or handle it as needed
    return 'XX'  # Replace with an appropriate default value

# Example usage:
# user_country = get_user_country(request)
# currency_symbol = get_currency_symbol(user_country)






def get_or_create_customer(request):
    if not request.user.is_authenticated:
        session_key = request.session.session_key
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                customer = session.customer
            except ObjectDoesNotExist:
                # Create new anonymous customer and link to session
                customer = Customer.objects.create()
                session.customer = customer
                session.save()
        else:
            # Create new session and anonymous customer
            request.session.create()
            customer = Customer.objects.create()
            request.session['customer_id'] = str(customer.id)
    else:
        customer = request.user.customer

    return customer
