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

travel_mode_time = {}

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

def get_travel_time(apiKey,location_list,mode_selected): # mode = walking, driving, bicycling, transit
    # car = 0.525 kg per hour
    # bus = 0.822 g per km
    import requests
    time = 0
    carbon_footprint = 0
    for i in range(len(location_list)-1):
        origin = location_list[i]
        destination = location_list[i+1]
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


if __name__ == '__main__':
    # get coordinates
    location_list = main()
    print(location_list)
    travel_times = get_travel_time(apiKey, location_list,mode_selected='transit')
    for x in travel_times:
        print(x,travel_times[x])
    # optimization_criteria = drive_time*carbon_footprint

