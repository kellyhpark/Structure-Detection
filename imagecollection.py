from dotenv import load_dotenv
import os
import requests
import hashlib
import hmac
import base64
import urllib.parse as urlparse

def sign_url(input_url=None, secret=None):
    # Sign a request URL with a URL signing secret.

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    # Return signed URL
    return "&signature=" + encoded_signature.decode()

load_dotenv()
api_key = os.getenv("API_KEY")
sign_key = os.getenv("SIGN_KEY")
url = os.getenv("URL")
api_secret = sign_url(url, sign_key)
print(api_secret)

request = requests.get(f"{url}size=600x400&location=32.86782,-117.231&fov=80&heading=70&pitch=0&key={api_key}{api_try}")
print(request)
with open("data/images/test1.jpg", "wb") as file:
    file.write(request.content)
request.close()