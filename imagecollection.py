import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("API_KEY")
# requests = requests.get("https://maps.googleapis.com/maps/api/streetview?size=600x400", \
#                         location=32.86782,-117.231, 
# &fov=80&heading=70&pitch=0&key=YOUR_API_KEY&signature=YOUR_SIGNATURE)
request = requests.get(f"https://maps.googleapis.com/maps/api/streetview?location=Z%C3%BCrich&size=600x400&location=32.86782,-117.231&fov=80&heading=70&pitch=0&key={api_key}")
with open('/data/images/test.jpg', 'wb') as file:
    file.write(request.content)
request.close()