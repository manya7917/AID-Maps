from graphh import GraphHopper
import folium
import requests

def distance(route_data):
    distance = round(route_data['distance'] / 1000, 2)
    print('Distance:', distance, 'km')

def time(route_data):
    time = round(route_data['time'] / 60000, 2)
    if(time > 60):
        print('Time:', time/60, 'Hours')
    else:
        print('Time:', time, 'Minutes')

def getCoords(response):
    data = response.json()    
    path = data['paths'][0]['points']['coordinates']
    pth=[]
    for i in range(len(path)):
        lon = path[i][0]
        laty = path[i][1]
        pth.append([laty, lon])
    return pth

def makemap(pth):
    folium.Marker(location=[lat1, long1], popup='Start', icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(location=[lat2, long2], popup='End', icon=folium.features.CustomIcon(icon_image='/Users/niharikarana/Desktop/car.png', icon_size=(50, 50))).add_to(m)
    folium.PolyLine(locations=pth, line_opacity = 0.5, color='red').add_to(m)
    m.save('car2.html')

    
#Main
endpoint = "https://graphhopper.com/api/1/route"
map_key = GraphHopper("key")

for i in range(1):
    origin = map_key.address_to_latlong(input("Enter Current loc: "))
    dest = map_key.address_to_latlong(input("Enter Destination loc: "))
    dist = map_key.distance([origin, dest], unit ='km')
    router = map_key.route([origin, dest])
    
    lat1 = router['paths'][0]['bbox'][1]
    long1 = router['paths'][0]['bbox'][0]
    lat2 = router['paths'][0]['bbox'][3]
    long2 = router['paths'][0]['bbox'][2]
    #print(lat1, long1, " : " ,lat2, long2)
    
    m = folium.Map(location =[lat1, long1], zoom_start = 10)
    
    st = str(lat1)+", "+ str(long1)
    en = str(lat2)+", "+ str(long2)
    print("Start : ", st)
    print("End : ", en)
    
    params = {
    "key": "key",
    "point": [st, en],
    "points_encoded": "false",
    "vehicle": "car",
    "locale": "en-US",
    "instructions": "false",
    "calc_points": "true"
    }

    # Send request to GraphHopper API
    response = requests.get(endpoint, params=params)

    #Get coordinates from Source to Destination
    pth = getCoords(response)
    #Making the map and saving it
    makemap(pth)

    #Printing ETA and Distance
    route_data = response.json()['paths'][0]
    
    distance(route_data)
    time(route_data)
    

    


