from django.core.validators import URLValidator


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except Exception as e:
        return False
