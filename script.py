

import requests
import sys
import grequests
import datetime

from math import sin, cos, sqrt, atan2, radians

def distance(x,y):
    # approximate radius of earth in km
    #print(x)
    R = 6373.0

    lat1 = radians(x[0])
    lon1 = radians(x[1])
    lat2 = radians(y[0])
    lon2 = radians(y[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    #print(distance)
    return distance * 1000

r = requests.get('http://localhost:5000/ecoles')
print(r)
ecoles = r.json()
#print(ecoles)
hectares = requests.get('http://localhost:5000/population').json()
hectares['features'] = hectares['features'][5090:]

best_ecoles = []
nbr_ec = len(ecoles['features'])

i = 0
offset = 1
with open('output_2901.csv', 'a') as out:
    while i + offset < len(hectares['features']):
        if i % 10 == 0:
            print(i)
            print(datetime.datetime.now())
        hect = hectares['features'][i:i+offset]
        p = []
        url = 'http://130.223.67.145:8080/otp/routers/ch/plan'
        ec = []
        for h in hect:
            coord_h = h['geometry']['coordinates']
            coord_h_str = str(coord_h[1]) + ',' + str(coord_h[0])
            
            param_req = []
           
            for j, e in enumerate(ecoles['features']):
                #print(j)
                coord_e = e['geometry']['coordinates']
                if distance([coord_e[1], coord_e[0]], [coord_h[1], coord_h[0]]) < 20000:
                    ec.append(e)
                    coord_e_str = str(coord_e[1]) + ',' + str(coord_e[0])
                    data = {
                        'toPlace': coord_e_str,
                        'fromPlace': coord_h_str,
                        'mode': 'CAR,WALK',
                        'numItineraries': 1
                    }
                    param_req.append(data)
                    data_inv = {
                        'toPlace': coord_h_str,
                        'fromPlace': coord_e_str,
                        'mode': 'CAR,WALK',
                        'numItineraries': 1
                    }
                    param_req.append(data_inv) 
            p += param_req
        rs = [grequests.get(url, params=p[i]) for i in range(0, len(p))]
        response = grequests.map(rs)
       
        #import ipdb; ipdb.set_trace()
        for j in range(0, len(hect)):
            #print((j+1)*nbr_ec*2)
            #print(response[j*nbr_ec*2:(j+1)*nbr_ec*2])
            times = [x.json().get('plan', {}).get('itineraries', [{}])[0].get('duration', sys.maxsize) if x is not None else sys.maxsize for x in response[j*len(ec)*2:(j+1)*len(ec)*2]]
            best_ec = times.index(min(times)) // 2
            coord = hect[j]['geometry']['coordinates']
            res = ec[best_ec]['properties']['id']
            t = min(times)
            #print(str(coord[1]) + ',' + str(coord[0]) + ';' + res + ';' + str(t) + ';' +  str(hect[j]['properties']['b14btot']))
            out.write(str(hect[j]['properties']['geocode']) + ';' + str(coord[1]) + ',' + str(coord[0]) + ';' + res + ';' + str(t) + ';' +  str(hect[j]['properties']['b14btot'])+ '\n');
            
        i += offset
    