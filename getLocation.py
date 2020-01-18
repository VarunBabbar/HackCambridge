from __future__ import print_function
import math
from quickstart import main
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


apiKey = 'AIzaSyA1HfqmvNY_qRHR_aV1JxDDcXKlQMWxuAo'



def get_lat_lng(apiKey, address):

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
    # car = 0.525 kg per hour
    # bus = 0.822 g per km
    import requests
    time = 0
    carbon_footprint = 0
    # url = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origin={}&destination={}&mode={}&key={}'
    #         #        .format(origin.replace(' ','+'),
    #         #                destination.replace(' ','+'),mode,
    #         #                str(apiKey)
    #         #                )
    #         #        )
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
        origin = location_list[i]
        destination = location_list[i+1]
        mode_time = get_travel_time(apiKey, origin, destination, mode_selected = 'transit')
        trips_today[i+1] = {
            "origin": origin,
            "destination": destination,
            "mode_time": mode_time
        }
    return trips_today
    

def getCo2emissions(origin, destination, mode):
    if mode== 'bicycling':
        return 0
    if mode == 'walking':
        return 0
    if mode == 'driving':
        time = get_drive_time(apiKey,origin,destination, mode)
        timearr = time.split(' ')
        hours = float(timearr[0])
        minutes = float(timearr[2])
        totaltime =  hours + (minutes / 60)
        co2 = totaltime*0.525
        return co2, totaltime
    # Get distance, time to between origin and destination

if __name__ == '__main__':
    # get coordinates
    location_list = main()
    print(location_list)
    legs = leg_travel_time(location_list)
    for x in legs:
        print(x,legs[x])
    arr = main()
    co2,totaltime = getCo2emissions(arr[0], arr[1],'driving')
    print(str(co2)  + " Kg of Co2 is emitted during the journey from " + arr[0] + " to " + arr[1] + ", which took " + str(totaltime) + " hours")
    # optimization_criteria = drive_time*carbon_footprint

