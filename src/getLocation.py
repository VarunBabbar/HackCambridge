from __future__ import print_function
import math
import requests
from quickstart import fetch_calendar
from json_parse import json_write
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

apiKey = 'AIzaSyA1HfqmvNY_qRHR_aV1JxDDcXKlQMWxuAo'
f = open('ResultMetrics.txt',"w+")

#emissions per second (kg per km)
RAIL = 2.8
METRO_RAIL = 6.9
SUBWAY = 4.5
TRAM = 5
MONORAIL = 5.4
HEAVY_RAIL = 6.02
COMMUTER_TRAIN = 6.5
HIGH_SPEED_TRAIN = 6.5
LONG_DISTANCE_TRAIN = 6.02
BUS = 5.5
INTERCITY_BUS = 6.9
TROLLEYBUS = 4.2
FERRY = 11.5
DRIVING = 17

def get_lat_lng(address):

    import requests
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
           .format(address.replace(' ','+'), apiKey))
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
    except:
        print('ERROR: {}'.format(address))
        lat = 0
        lng = 0
    return lat, lng

def get_travel_time(apiKey,origin,destination,mode_selected):
    travel_mode_time = {}
    # car = 0.525 kg per hour per person
    # bus = 0.822 g per km per person
    # heavy rail = 1 kg per hour per person

    url = ('https://maps.googleapis.com/maps/api/directions/json?units=imperial&origin={}&destination={}&mode={}&key={}'
        .format(origin.replace(' ','+'),
                destination.replace(' ','+'),mode_selected,
                str(apiKey)
                )
            )
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        step_list = resp_json_payload["routes"][0]["legs"][0]["steps"]
        for step in step_list:
            duration = step["duration"]["value"]
            mode = step["travel_mode"]
            if mode=="TRANSIT":
                mode = step["transit_details"]["line"]["vehicle"]["type"]
            if mode in travel_mode_time:
                travel_mode_time[mode] = travel_mode_time[mode] + duration
            else:
                travel_mode_time[mode] = duration
    except:
        print('ERROR: {}, {}'.format(origin, destination))
    return travel_mode_time

def leg_travel_time(location_list,mode): # mode = walking, driving, bicycling, transit
    trips_today = {}
    for i in range(0,len(location_list)-1):
        origin_address = location_list[i]
        origin_lat,origin_lng = get_lat_lng(origin_address)
        destination_address = location_list[i+1]
        destination_lat,destination_lng = get_lat_lng(destination_address)
        mode_time = get_travel_time(apiKey, origin_address, destination_address, mode_selected = mode)
        trips_today[i+1] = {
            "origin": {
                "addresss": origin_address,
                "lat": origin_lat,
                "lng": origin_lng
                },
            "destination": {
                "address": destination_address,
                "lat": destination_lat,
                "lng": destination_lng,
                },
            "mode_time": mode_time
        }
    return trips_today


def getCo2emissions(legs,mode):
    for leg in legs:
        legx = legs[leg]
        mode_types = legx['mode_time']
        railtime = 0
        meterorailtime = 0
        subwaytime = 0
        tramtime = 0
        monorailtime = 0
        heavyrailtime = 0
        commutertraintime = 0
        highspeedtraintime = 0
        longdistancetraintime = 0
        bustime = 0
        intercitybustime = 0
        trolleybustime = 0
        ferrytime = 0
        drivingtime = 0
        walktime = 0
        bicyclingtime = 0
        for i in list(mode_types.keys()):
            if i == 'RAIL':
                railtime += mode_types[i]
            if i == 'METRO_RAIL':
                meterorailtime += mode_types[i]
            if i == 'SUBWAY':
                subwaytime += mode_types[i]
            if i == 'TRAM':
                tramtime += mode_types[i]
            if i == 'MONORAIL':
                monorailtime += mode_types[i]
            if i == 'HEAVY_RAIL':
                heavyrailtime += mode_types[i]
            if i == 'COMMUTER_TRAIN':
                commutertraintime += mode_types[i]
            if i == 'HIGH_SPEED_TRAIN':
                highspeedtraintime += mode_types[i]
            if i == 'LONG_DISTANCE_TRAIN':
                longdistancetraintime += mode_types[i]
            if i == 'BUS':
                bustime += mode_types[i]
            if i == 'INTERCITY_BUS':
                intercitybustime += mode_types[i]
            if i == 'TROLLEYBUS':
                trolleybustime += mode_types[i]
            if i == 'FERRY':
                ferrytime += mode_types[i]
            if i == 'DRIVING':
                drivingtime += mode_types[i]
            if i == 'BICYCLING':
                bicyclingtime += mode_types[i]
            if i == 'WALKING':
                bicyclingtime += mode_types[i]
        railco2 = railtime*RAIL
        meterorailco2 = meterorailtime*METRO_RAIL
        subwayco2 = subwaytime*SUBWAY
        tramco2 = tramtime*METRO_RAIL
        monorailco2 = monorailtime*METRO_RAIL
        heavyrailco2 = heavyrailtime*METRO_RAIL
        commuterrailco2 = commutertraintime*METRO_RAIL
        highspeedtrainco2 = highspeedtraintime*METRO_RAIL
        longdistancetrainco2 = longdistancetraintime*METRO_RAIL
        busco2 = bustime*METRO_RAIL
        intercitybusco2 = intercitybustime*METRO_RAIL
        trolleybusco2 = trolleybustime*METRO_RAIL
        ferryco2 = ferrytime*METRO_RAIL
        drivingco2 = drivingtime*DRIVING
        lol = {'RAIL':railco2, 'METRO_RAIL':meterorailco2, 'SUBWAY':subwayco2,'TRAM':tramco2,
                                  'MONORAIL':monorailco2,'HEAVY_RAIL':heavyrailco2,'COMMUTER_TRAIN':commuterrailco2,
                                  'HIGH_SPEED_TRAIN':highspeedtrainco2,'LONG_DISTANCE_TRAIN':longdistancetrainco2,'BUS':busco2,'INTERCITY_BUS':intercitybusco2,
                                  'TROLLEYBUS':trolleybusco2,'FERRY':ferryco2,'WALKING':0,'BICYCLING':0,'DRIVING':drivingco2}
        emissionsdict = {}
        for i in mode_types:
            emissionsdict[i] = lol[i]
        legx['mode_emissions'] = emissionsdict
        print((railtime + meterorailtime+subwaytime+tramtime+monorailtime+heavyrailtime+commutertraintime+highspeedtraintime +
               longdistancetraintime+bustime+intercitybustime+trolleybustime+ferrytime+drivingtime + walktime + bicyclingtime))
        if (railco2+meterorailco2+subwayco2+tramco2+monorailco2+heavyrailco2+commuterrailco2+highspeedtrainco2+longdistancetrainco2+
              busco2+intercitybusco2+trolleybusco2+ferryco2+drivingco2) == 0:
            if (railtime + meterorailtime+subwaytime+tramtime+monorailtime+heavyrailtime+commutertraintime+highspeedtraintime +
                longdistancetraintime+bustime+intercitybustime+trolleybustime+ferrytime+drivingtime + walktime + bicyclingtime) == 0:
                legx['efficiency'] = "Undefined"
            else:
                legx['efficiency'] = 1000000000 / ((railtime + meterorailtime+subwaytime+tramtime+monorailtime+heavyrailtime+commutertraintime+highspeedtraintime +
                                                   longdistancetraintime+bustime+intercitybustime+trolleybustime+ferrytime+drivingtime + walktime + bicyclingtime)*10000)
        else:
            legx['efficiency'] = 1000000000/((railtime + meterorailtime+subwaytime+tramtime+monorailtime+heavyrailtime+commutertraintime+highspeedtraintime +
                                              longdistancetraintime+bustime+intercitybustime+trolleybustime+ferrytime+drivingtime + walktime + bicyclingtime)
                                             *(railco2+meterorailco2+subwayco2+tramco2+monorailco2+heavyrailco2+commuterrailco2+highspeedtrainco2+longdistancetrainco2+
                                               busco2+intercitybusco2+trolleybusco2+ferryco2+drivingco2))
        f.write("Leg" + str(leg) + " Mode = " + str(mode) + str(legx) + '\r\n')
    # Get distance, time to between origin and destination
    # print(legs)
    return legs
def efficiency_scorer():
    location_list = fetch_calendar()
    lat,lng = get_lat_lng(location_list[0])
    legs = getCo2emissions(leg_travel_time(location_list,'walking'),'walking')
    try:
        walktime = 0
        for leg in legs:
            walktime +=legs[leg]['mode_time']['WALKING']
    except:
        print("No Walking Route Found")
        walktime = 10**6
    legs = getCo2emissions(leg_travel_time(location_list,'driving'),'driving')
    drivetime = 0
    driveco2 = 0
    for leg in legs:
        drivetime += legs[leg]['mode_time']['DRIVING']
        driveco2 += legs[leg]['mode_emissions']['DRIVING']
    legs = getCo2emissions(leg_travel_time(location_list,'bicycling'),'bicycling')
    try:
        cycletime = 0
        for leg in legs:
            cycletime += legs[leg]['mode_time']['BICYCLING']
    except:
        print("No Cycling Route Found")
        cycletime = 10**6
    legs = getCo2emissions(leg_travel_time(location_list,'transit'),'transit')
    totaltime = 0
    totalco2 = 0
    for leg in legs:
        mode_time = legs[leg]['mode_time']
        for i in mode_time.keys():
            totaltime += mode_time[i]
            totalco2 += legs[leg]['mode_emissions'][i]
    json_write(legs[1])

    return walktime,drivetime,driveco2,cycletime,totaltime,totalco2

    # optimization_criteria = drive_time*carbon_footprint
walktime,drivetime,driveco2,cycletime,totaltime,totalco2 = efficiency_scorer()

f.write('\r\n')
f.write('================================================================================================================\r\n')

f.write('\r\n')
if walktime != 10**6:
    print("Total Time Spent if only Walking (hours) = " + str(walktime/3600))
    f.write("Total Time Spent if only Walking (hours) = " + str(walktime/3600)+ '\r\n')
    f.write('\r\n')
if cycletime != 10**6:
    print("Total Time Spent if only Cycling (hours) = " + str(cycletime/3600))
    f.write("Total Time Spent if only Cycling (hours) = " + str(cycletime/3600)+ '\r\n')
    f.write('\r\n')
f.write('================================================================================================================\r\n')

f.write('\r\n')
print("Total Time Spent if only Driving (hours) = " + str(drivetime/3600))
f.write("Total Time Spent if only Driving (hours) = " + str(drivetime/3600)+ '\r\n')

f.write('\r\n')
print("Total CO2 emitted for only Driving (kg) = " + str(driveco2))
f.write("Total CO2 emitted for only Driving (kg) = " + str(driveco2) + '\r\n')

f.write('\r\n')
f.write('================================================================================================================\r\n')

f.write('\r\n')
print("Total Time Taken if transit option taken (hours) = " + str(totaltime/3600))
f.write("Total Time Taken if transit option taken (hours) = " + str(totaltime/3600)+ '\r\n')
f.write('\r\n')
print("Total CO2 Emitted if transit option taken (kg) = " + str(totalco2))
f.write("Total CO2 Emitted if transit option taken (hours) = " + str(totalco2)+ '\r\n')
f.write('\r\n')

f.write('================================================================================================================\r\n')

f.write('\r\n')
if walktime != 10**6:
    print("Efficiency Metric for Only Walking: " + str(1000000000/(driveco2*walktime)))
    f.write("Efficiency Metric for Only Walking:" + str(1000000000/(driveco2*walktime)) + '\r\n')
    f.write('\r\n')
else:
    print("Efficiency Metric for Only Walking: 0")
    f.write("Efficiency Metric for Only Walking: 0")
    f.write('\r\n')
    f.write('\r\n')
if cycletime != 10**6:
    f.write("Efficiency Metric for Only Cycling: " + str(1000000000/(driveco2*cycletime))+ '\r\n')
    f.write('\r\n')
else:
    print("Efficiency Metric for Only Cycling: 0")
    f.write("Efficiency Metric for Only Cycling: 0")
    f.write('\r\n')

print("Efficiency Metric for Only Driving: " + str(1000000000/(driveco2*drivetime)))
f.write("Efficiency Metric for Only Driving: " + str(1000000000/(driveco2*drivetime))+ '\r\n')
f.write('\r\n')
if totalco2 != 0:
    print("Efficiency Metric for Transit: " + str(1000000000/(totaltime*totalco2)))
    f.write("Efficiency Metric for Transit: " + str(1000000000/(totaltime*totalco2))+ '\r\n')
    f.write('\r\n')
else:
    print("Efficiency Metric for Transit: " + str(1000000000/(totaltime*driveco2)))
    f.write("Efficiency Metric for Transit: " + str(1000000000/(totaltime*driveco2))+ '\r\n')
    f.write('\r\n')
f.write('================================================================================================================\r\n')
