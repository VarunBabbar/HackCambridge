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

def get_drive_time(apiKey,arr,mode): # mode = walking, driving, bicycling, transit
    # car = 0.525 kg per hour
    # bus = 0.822 g per km
    import requests
    time = 0
    carbon_footprint = 0
    for i in range(len(arr)-1):
        origin = arr[i]
        destination = arr[i+1]
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&mode={}&key={}'
               .format(origin.replace(' ','+'),
                       destination.replace(' ','+'),mode,
                       str(apiKey)
                       )
               )
        try:
            response = requests.get(url)
            resp_json_payload = response.json()
            time += math.ceil(resp_json_payload['rows'][0]['elements'][0]['duration']['value'])
        except:
            print('ERROR: {}, {}'.format(origin, destination))
        time = time
    return time


if __name__ == '__main__':
    # get coordinates
    arr = main()
    print(arr)
    drive_time = get_drive_time(apiKey, arr,'transit')
    print(drive_time)
    # optimization_criteria = drive_time*carbon_footprint

