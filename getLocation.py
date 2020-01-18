apiKey = 'AIzaSyA1HfqmvNY_qRHR_aV1JxDDcXKlQMWxuAo'
import math
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

# if __name__ == '__main__':
#     # get ke
#
#     # get coordinates
#     address = '1 Rocket Road, Hawthorne, CA'
#     lat, lng = get_lat_lng(apiKey, address)
#     print(lat, lng)
# AIzaSyA1HfqmvNY_qRHR_aV1JxDDcXKlQMWxuAo


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
                       apiKey
                       )
               )
        try:
            response = requests.get(url)
            resp_json_payload = response.json()
            print(resp_json_payload)
            time += math.ceil(resp_json_payload['rows'][0]['elements'][0]['duration']['value'])
        except:
            print('ERROR: {}, {}'.format(origin, destination))
        time = time
    return time


if __name__ == '__main__':
    # get coordinates
    origin = 'Buckhingham Palace, UK'
    destination = 'Queens College, University of Cambridge, Cambridge CB3 9ET, UK'
    arr = [origin,destination]
    drive_time = get_drive_time(apiKey, arr,'transit')
    print('Origin: {}\nDestination: {}\nDrive Time:  {} min'.format(origin, destination, drive_time/60))
    # optimization_criteria = drive_time*carbon_footprint

# def getTimesforeachroute(arr):
