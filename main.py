import time
import googlemaps # pip install googlemaps
import pandas as pd # pip install pandas
import globals
        
API_KEY = globals.API_KEY
map_client = googlemaps.Client(API_KEY)

address = globals.address
geocode = map_client.geocode(address=address)
(lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))
search = 'restaurants'
distance = 1000
restaurants = []

response = map_client.places_nearby(
    location=(lat, lng),
    keyword=search,
    radius=distance
)   

restaurants.extend(response.get('results'))
next_page_token = response.get('next_page_token')

while next_page_token:
    time.sleep(2)
    response = map_client.places_nearby(
        location=(lat, lng),
        keyword=search,
        radius=distance,
        page_token=next_page_token
    )  
    restaurants.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

df = pd.DataFrame.from_records(restaurants) 
df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']



mask = ['business_status', 'geometry', 'icon', 'icon_background_color',
        'icon_mask_base_uri', 'opening_hours', 'photos', 'place_id', 'plus_code', 
        'reference', 'scope', 'types']
df.drop(mask, axis=1, inplace=True)
df.to_csv('restaurants.csv')