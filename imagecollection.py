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

def image_generator(coords, heading, fov, pitch, structure_pic):
    url = f"{base_url}size=600x400&location={coords[0]},{coords[1]}&fov={fov}&heading={heading}&pitch={pitch}&key={api_key}"
    api_secret = sign_url(url, sign_key)
    request = requests.get(api_secret)
    if (request.ok == True):
        pic_name = f"data/images/structure{structure_pic}.jpg"
        with open(pic_name, "wb") as file:
            file.write(request.content)
        request.close()
        plt.figure()
        img=mpimg.imread(pic_name)
        imgplot = plt.imshow(img)
        plt.show()

def image_params(params, structure_num):
    img_count = 15
    for i in range(img_count):
        lat_coord = params[i][0]
        long_coord = params[i][1]
        heading = params[i][2]
        fov = params[i][3]
        pitch = params[i][4]
        structure_pic = f"{structure_num}_{i+1}"
        image_generator((lat_coord, long_coord), heading, fov, pitch, structure_pic)

struc1 = [[32.8678091, -117.2316809, 104.74, 90, 0],[32.8678091, -117.2316809, 104.74, 50, 0],\
          [32.8678091, -117.2316809, 104.74, 20, -2],[32.867829, -117.2315762, 120.09, 90, 0],\
          [32.867829, -117.2315762, 120.09, 50, 0],[32.867829, -117.2315762, 120.09, 20, -8],\
           [32.8678515, -117.2314751, 185.27, 90, 0],[32.8678515, -117.2314751, 185.27, 50, 0],\
	    [32.8678515, -117.2314751, 185.27, 20, -9], [32.8678702, -117.2313684, 218.15, 90, 0],\
	    [32.8678702, -117.2313684, 218.15, 50, 0],[32.8678702, -117.2313684, 221, 20, -3],\
        [32.8678689, -117.2312877, 239.82, 90, 0],[32.8678689, -117.2312877, 239.82, 50, 0],\
	    [32.8678689, -117.2312877, 239.82, 20, 0]]
