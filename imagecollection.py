from dotenv import load_dotenv
import os
import requests
import hashlib
import hmac
import base64
import urllib.parse as urlparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()

load_dotenv()
api_key = os.getenv("API_KEY")
sign_key = os.getenv("SIGN_KEY")
base_url = os.getenv("URL")
url = f"{base_url}size=600x400&location=32.86782,-117.231&fov=80&heading=70&pitch=0&key={api_key}"
api_secret = sign_url(url, sign_key)
request = requests.get(api_secret)
print(request)


# request = requests.get(f"{url}size=600x400&location=32.86782,-117.231&fov=80&heading=70&pitch=0&key={api_key}{api_secret}")
# print(request)
# print(f"{url}size=600x400&location=32.86782,-117.231&fov=80&heading=70&pitch=0&key={api_key}{api_secret}")

lat_coord = 32.85631
long_coord = -117.207
heading = 165
fov = 70
pitch = 0
request = requests.get(f"{url}size=600x400&location={lat_coord},{long_coord}&fov={fov}&heading={heading}&pitch={pitch}&key={api_key}")
print(request)
if (request.ok == True):
    pic_name = f"data/images/test{5}.jpg"
    with open(pic_name, "wb") as file:
        file.write(request.content)
    request.close()
    plt.figure()
    img=mpimg.imread(pic_name)
    imgplot = plt.imshow(img)
    plt.show()