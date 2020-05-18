import facebook
import urllib
import json
import datetime as dt
from operator import attrgetter
import gui

# This function formats the datetime values to more pleasing format.
def formatEventDateTime(datetime):
    datetime = datetime.replace('T', '')
    date = datetime[0:10]
    date = dt.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    time = datetime[10:15]
    formatedDateTime = {'date': date, 'time': time}
    return formatedDateTime

#Storing the image from api locally so it can be rendered to the user interface.
def storeProfilePictureLocally(pic):
    picUrl = pic
    urllib.request.urlretrieve(picUrl, r'images\ProfilePicture.png')

def generateArrayOfEvents(events, profileObj):
    numberOfEvents = len(profileObj['events']['data'])
    for e in range(numberOfEvents):
        try:
            cut = slice(-8)
            event = {
                'eventName': profileObj['events']['data'][e]['name'],
                'eventPlace': profileObj['events']['data'][e]['place']['name'],
                'startTime': profileObj['events']['data'][e]['start_time'][cut],
            }

            keys = profileObj['events']['data'][e].keys()

            if 'end_time' in keys:
                event.update({'endTime': profileObj['events']['data'][e]['end_time'][cut]})
                eventEnds = formatEventDateTime(event['endTime'])
                eventStarts = formatEventDateTime(event['startTime'])
                event.update([('eventStarts', eventStarts), ('eventEnds', eventEnds)])
                del event['endTime']
            else:
                event.update({'endTime': 'Not Available'})
                eventStarts = formatEventDateTime(event['startTime'])
                event.update([('eventStarts', eventStarts)])

            del event['startTime']
            events.append(event)
        except UnicodeEncodeError:
            print('There was an error encoding the facebook event!')
            
    return events

def fetchFromGraphAPI(events):
    token = {'EAAJyBpwkDxMBAFaobfwU2OB8mpIo0VLbZC7Mj7Yu562xyULrqmauBVqwxQ44AKwjwQcspNIDO7Eh0ZBcxBgZAkTeK437iRZAtqCXhRMCR6B4RZA2emxNcHFB25MtfXNZA9SM1o6kVxZCZCEkLp1P3899ah72oWZC5KZC5T2fcw5PH9v6nLNUmHy1VOiShvMFYZA08HZBFQ3pIeczd464qV4bJEpTXyBcJR10GkZCsZCa2FZCjK2IQZDZD'}
    graph = facebook.GraphAPI(token)

    #This is the representation of the events object from the api.
    profile = graph.get_object('me', fields ='picture,events')

    #Storing the fb profile picture with the function written.
    profilePicture = profile['picture']['data']['url']
    storeProfilePictureLocally(profilePicture)
    
    return generateArrayOfEvents(events, profile)


def main():
    # Creating events array, filling it with the data from the fetch function and
    # sending it to the gui module for rendering.
    events = []
    events = fetchFromGraphAPI(events)
    gui.tkinter(events)

if __name__ == "__main__":
    main()