from datetime import timedelta

# Choose your preferred method for remember me functionality
# If using cookies:
# from django.http import response

# If using sessions:
from django.contrib.sessions.models import Session


def set_remember_me_cookie(request, user):
    # Conditional import based on chosen method
    # If using cookies:
    # try:
    #     response = response
    # except NameError:
    #     raise ImportError("Remember Me functionality requires 'response' from django.http")

    # If using sessions:
    try:
        request.session
    except AttributeError:
        raise ImportError("Remember Me functionality requires 'session' from django.contrib.sessions")

    # Set cookie or session based on chosen method
    # If using cookies:
    #     response.set_cookie(
    #         key="remember_me",
    #         value=user.pk,
    #         expires=datetime.utcnow() + timedelta(days=30),
    #         secure=True,
    #     )

    # If using sessions:
    request.session['remember_me'] = user.pk
    request.session.set_expiry(60 * 60 * 24 * 30)  # Expires in 30 days

    # Alternatively, set a specific expiry date for sessions
    # request.session.set_expiry(datetime.utcnow() + timedelta(days=30))
