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
    # Returns a full url usable for dynamic API requests with a converted secret signature
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

# Load the .env file
load_dotenv()
# Call the variables in the .env file
api_key = os.getenv("API_KEY")
sign_key = os.getenv("SIGN_KEY")
base_url = os.getenv("URL")

def image_generator(base_url, sign_key, api_key, coords, heading, fov, pitch, structure_pic):
    # Receives parameters needed for an API request, and requests and saves the image
    url = f"{base_url}size=600x400&location={coords[0]},{coords[1]}&fov={fov}&heading={heading}&pitch={pitch}&key={api_key}"
    api_secret = sign_url(url, sign_key)
    request = requests.get(api_secret)
    # If request is successful, save the image with a unique name and display image
    if (request.ok == True):
        pic_name = f"data/images/structure{structure_pic}.jpg"
        with open(pic_name, "wb") as file:
            file.write(request.content)
        request.close()

def image_params(base_url, sign_key, api_key, params, structure_num):
    # Takes a structure and its 15 unique set of parameters for different image angles and calls the function to save those images
    img_count = 15
    for i in range(img_count):
        lat_coord = params[i][0]
        long_coord = params[i][1]
        heading = params[i][2]
        fov = params[i][3]
        pitch = params[i][4]
        structure_pic = f"{structure_num}_{i+1}"
        # Call the image generator function to make an api request and save img
        image_generator(base_url, sign_key, api_key, (lat_coord, long_coord), heading, fov, pitch, structure_pic)

struc1 = [[32.8678091, -117.2316809, 104.74, 90, 0],[32.8678091, -117.2316809, 104.74, 50, 0],\
        [32.8678091, -117.2316809, 104.74, 20, -2],[32.867829, -117.2315762, 120.09, 90, 0],\
        [32.867829, -117.2315762, 120.09, 50, 0],[32.867829, -117.2315762, 120.09, 20, -8],\
        [32.8678515, -117.2314751, 185.27, 90, 0],[32.8678515, -117.2314751, 185.27, 50, 0],\
	    [32.8678515, -117.2314751, 185.27, 20, -9], [32.8678702, -117.2313684, 218.15, 90, 0],\
	    [32.8678702, -117.2313684, 218.15, 50, 0],[32.8678702, -117.2313684, 221, 20, -3],\
        [32.8678689, -117.2312877, 239.82, 90, 0],[32.8678689, -117.2312877, 239.82, 50, 0],\
	    [32.8678689, -117.2312877, 239.82, 20, 0]]

struc2 = [[32.870376, -117.215102, 219.93, 90, 0],[32.870376, -117.215102, 219.93, 50, 0],
	[32.870376, -117.215102, 219.93, 10, 0],[32.8703091, -117.2151368, 225.7, 90, 0],
	[32.8703091, -117.2151368, 225.7, 50, 0],[32.8703091, -117.2151368, 229, 10, -2],
    [32.8702251, -117.2152133, 237.11, 90, 0],[32.8702251, -117.2152133, 237.11, 50, 0],
	[32.8702251, -117.2152133, 241, 20, -5],[32.8700988, -117.215256, 333.43, 90, 0],
	[32.8700988, -117.215256, 333.43, 50, 0],[32.8700988, -117.215256, 333.43, 15, -8],
    [32.8699886, -117.2152565, 342.63, 90, 0],[32.8699886, -117.2152565, 342.63, 30, 0],
	[32.8699886, -117.2152565, 355, 10, 0]]

struc3 = [[32.8690534, -117.2164373, 316.44, 80, 0],
	[32.8690534, -117.2164373, 316.44, 50, 0],[32.8690534, -117.2164373, 310.44, 20, 0],
    [32.869096, -117.2165479, 332.86, 80, 0],[32.869096, -117.2165479, 332.86, 50, 0],
	[32.869096, -117.2165479, 320, 20, -3],[32.8691188, -117.2166037, 347.64, 90, 0],
	[32.8691188, -117.2166037, 347.64, 50, 0],[32.8691188, -117.2166037, 340.64, 20, -10],
    [32.869158, -117.2167074, 49.12, 90, 0],[32.869158, -117.2167074, 49.12, 50, 0],
	[32.869158, -117.2167074, 52, 20, -9],[32.8691807, -117.2168236, 72.43, 90, 0],
	[32.8691807, -117.2168236, 72.43, 50, 0],[32.8691807, -117.2168236, 74, 15, -5]]

struc4 = [[32.8701057, -117.2164061, 30.52, 90, 0],[32.8701057, -117.2164061, 34, 50, 0],
    [32.8701057, -117.2164061, 52, 10, -6],[32.8701856, -117.2163589, 86.85, 90, 0],
	[32.8701856, -117.2163589, 86.85, 50, 0],[32.8701856, -117.2163589, 80, 20, -10],
    [32.8702685, -117.2163187, 141.76, 90, 0],[32.8702685, -117.2163187, 141.76, 50, 0],
	[32.8702685, -117.2163187, 141.76, 20, -10],[32.8703481, -117.2162726, 170.38, 90, 0],
	[32.8703481, -117.2162726, 170.38, 50, 0],[32.8703481, -117.2162726, 173, 15, -5],
    [32.8703877, -117.2162885, 173.33, 70, 0],[32.8703877, -117.2162885, 173.33, 40, 0],
    [32.8703877, -117.2162885, 173.33, 15, -6]]

struc5 = [[32.8698186, -117.2146501, 107.91, 90, 0],[32.8698186, -117.2146501, 107.91, 50, 0],
	[32.8698186, -117.2146501, 107.91, 15, -3],[32.8698191, -117.2145515, 111.21, 90, 0],
	[32.8698191, -117.2145515, 111.21, 50, 0],[32.8698191, -117.2145515, 111.21, 15, -6],
    [32.8698172, -117.2144486, 155.63, 90, 0],[32.8698172, -117.2144486, 155.63, 50, -8],
	[32.8698172, -117.2144486, 140, 22, -18],[32.8698009, -117.2142995, 246.52, 90, 0],
	[32.8698009, -117.2142995, 246.52, 50, 0],[32.8698009, -117.2142995, 260, 15, -4],
    [32.8697639, -117.2141577, 285.24, 90, 0],[32.8697639, -117.2141577, 285.24, 50, 0],
	[32.8697639, -117.2141577, 270, 15, -3]]

struc6 = [[32.8560624, -117.2065994, 335.67, 90, 0],[32.8560624, -117.2065994, 335.67, 30, 0],
	[32.8560624, -117.2065994, 337, 15, 0],[32.8561433, -117.2066486, 332.27, 90, 0],
	[32.8561433, -117.2066486, 332.27, 30, 0],[32.8561433, -117.2066486, 340, 15, -1],
    [32.856221, -117.206703, 352.94, 90, 0],[32.856221, -117.206703, 352.94, 30, 0],
	[32.856221, -117.206703, 355, 20, 0],[32.8562953, -117.206764, 67.15, 90, 0],
	[32.8562953, -117.206764, 67.15, 50, 0],[32.8562953, -117.206764, 67.15, 20, -5],
    [32.856366, -117.2068317, 112.07, 90, 0],[32.856366, -117.2068317, 112.07, 50, 0],
	[32.856366, -117.2068317, 112.07, 15, 0]]

struc7 = [[32.8567326, -117.2073275, 329.63, 90, 0],[32.8567326, -117.2073275, 329.63, 50, 0],
	[32.8567326, -117.2073275, 329.63, 15, -3],[32.8567907, -117.2074086, 340.85, 90, 0],
	[32.8567907, -117.2074086, 340.85, 50, 0],[32.8567907, -117.2074086, 345, 20, -3],
    [32.856843, -117.2074805, 49.54, 90, 0],[32.856843, -117.2074805, 49.54, 50, 0],
	[32.856843, -117.2074805, 70, 20, -4],[32.8568749, -117.2075341, 77.12, 90, 0],
	[32.8568749, -117.2075341, 77.12, 50, 0],[32.8568749, -117.2075341, 95, 15, 0],
    [32.85693, -117.207621, 101.4, 90, 0],[32.85693, -117.207621, 101.4, 50, 0],
	[32.85693, -117.207621, 110, 15, 0]]

struc8 = [[32.857206, -117.2094367, 17.86, 90, 0],[32.857206, -117.2094367, 17.86, 50, 0],
	[32.857206, -117.2094367, 17.86, 15, 0],[32.857302, -117.2094385, 41.03, 90, 0],
	[32.857302, -117.2094385, 41.03, 50, 0],[32.857302, -117.2094385, 38, 15, 0],
    [32.8573927, -117.2094358, 87.97, 90, 0],[32.8573927, -117.2094358, 87.97, 50, 0],
	[32.8573927, -117.2094358, 89, 15, -4],[32.8574836, -117.2094337, 130.97, 90, 0],
	[32.8574836, -117.2094337, 130.97, 50, 0],[32.8574836, -117.2094337, 150, 15, 0],
    [32.857576, -117.2094344, 148.59, 90, 0],[32.857576, -117.2094344, 148.59, 50, 0],
	[32.857576, -117.2094344, 165, 10, 0]]

struc9 = [[32.8556612, -117.2094483, 21.98, 90, 0],[32.8556612, -117.2094483, 21.98, 50, 0],
	[32.8556612, -117.2094483, 15, 10, 0],[32.8558131, -117.209457, 41.31, 90, 0],
	[32.8558131, -117.209457, 41.31, 50, 0],[32.8558131, -117.209457, 41.31, 90, 0],
    [32.8558162, -117.2097261, 77.48, 60, 0],[32.8558162, -117.2097261, 77.48, 30, 2],
	[32.8558162, -117.2097261, 77.48, 15, 2],[32.8560192, -117.2094434, 148.46, 90, 0],
	[32.8560192, -117.2094434, 148.46, 50, 0],[32.8560192, -117.2094434, 155, 20, 0],
    [32.8561073, -117.2094441, 161.98, 90, 0],[32.8561073, -117.2094441, 161.98, 50, 0],
	[32.8561073, -117.2094441, 161.98, 15, -1]]

struc10 = [[32.8660664, -117.2371056, 186.63, 90, 0],[32.8660664, -117.2371056, 186.63, 50, 10],
	[32.8660664, -117.2371056, 195, 20, 20],[32.8659512, -117.2370748, 212.47, 90, 0],
	[32.8659512, -117.2370748, 205, 50, 9],[32.8659512, -117.2370748, 200, 20, 20],
    [32.86584, -117.2370756, 259.27, 90, 20],[32.86584, -117.2370756, 259.27, 50, 20],
	[32.86584, -117.2370756, 260, 30, 8],[32.8657595, -117.2371837, 358.23, 90, 10],
	[32.8657595, -117.2371837, 358.23, 50, 10],[32.8657595, -117.2371837, 358.23, 20, 5],
    [32.8656763, -117.2371601, 343.14, 90, 0],[32.8656763, -117.2371601, 343.14, 50, 5],
	[32.8656763, -117.2371601, 348, 20, 0]]

structures = [struc1, struc2, struc3, struc4, struc5, struc6, struc7, struc8, struc9, struc10]
for i in range(len(structures)):
    # For each of the 10 structures, call image_params to begin saving pictures of the different angles
    structure_num = i+1
    image_params(base_url, sign_key, api_key, structures[i], structure_num)