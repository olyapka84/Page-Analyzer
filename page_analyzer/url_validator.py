from urllib.parse import urlparse
import validators


def is_valid_url(url):
    return validators.url(url) and len(url) <= 255


def normalize_url(url):
    return urlparse(url)._replace(path='', query='', fragment='').geturl()
