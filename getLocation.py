from __future__ import print_function
import math
from quickstart import fetch_calendar
from json_parse import json_write
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


apiKey = 'AIzaSyA1HfqmvNY_qRHR_aV1JxDDcXKlQMWxuAo'

#emissions per second
RAIL = 2
METRO_RAIL = 3
SUBWAY = 1
TRAM = 5
MONORAIL = 1.5
HEAVY_RAIL = 7
COMMUTER_TRAIN = 2.3
HIGH_SPEED_TRAIN = 4.1
LONG_DISTANCE_TRAIN = 3.4
BUS = 0.9
INTERCITY_BUS = 0.8
TROLLEYBUS = 10.1
FERRY = 4.5

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

def get_travel_time(apiKey,origin,destination,mode_selected): # mode = walking, driving, bicycling, transit
    travel_mode_time = {}
    # car = 0.525 kg per hour per person
    # bus = 0.822 g per km per person
    # heavy rail = 1 kg per hour per person
    import requests
    
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

def leg_travel_time(location_list):
    trips_today = {}
    for i in range(0,len(location_list)-1):
        origin_address = location_list[i]
        origin_lat,origin_lng = get_lat_lng(origin_address)
        destination_address = location_list[i+1]
        destination_lat,destination_lng = get_lat_lng(destination_address)
        mode_time = get_travel_time(apiKey, origin_address, destination_address, mode_selected = 'transit')
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
    

def getCo2emissions(legs):
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
        lol = {'RAIL':railco2, 'METRO_RAIL':meterorailco2, 'SUBWAY':subwayco2,'TRAM':tramco2,
                                  'MONORAIL':monorailco2,'HEAVY_RAIL':heavyrailco2,'COMMUTER_TRAIN':commuterrailco2,
                                  'HIGH_SPEED_TRAIN':highspeedtrainco2,'LONG_DISTANCE_TRAIN':longdistancetrainco2,'BUS':busco2,'INTERCITY_BUS':intercitybusco2,
                                  'TROLLEYBUS':trolleybusco2,'FERRY':ferryco2}
        emissionsdict = {key:val for key,val in lol.items() if val !=0}
        legx['mode_emissions'] = emissionsdict
    # Get distance, time to between origin and destination
    return legs

if __name__ == '__main__':
    # get coordinates
    location_list = fetch_calendar()
    lat,lng = get_lat_lng(location_list[0])
    print(lat,lng)
    legs = getCo2emissions(leg_travel_time(location_list))
    for leg in legs:
        print(leg,legs[leg])
    arr = fetch_calendar()
    json_write(legs)

    # optimization_criteria = drive_time*carbon_footprint

