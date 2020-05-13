import tkinter as tk
import facebook
import pybase64
import urllib
import json
from PIL import ImageTk, Image
import datetime as dt
from operator import attrgetter
from colour import Color

def formatEventDateTime(datetime):
    datetime = datetime.replace('T', '')
    date = datetime[0:10]
    date = dt.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    time = datetime[10:15]
    formatedDateTime = {'date': date, 'time': time}
    return formatedDateTime

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
    token = {'EAAJyBpwkDxMBAHrBg4nPVer47kWi2MUYbXNFW5hIi2d6AHdQKPXIFgeOzZA9JHzP4mujHjWLSLZAHeNfAdnpgMHP1tQNh9MfUArQs8TOmRZC6nufBG1tzM46u1c0Y96gffSfHrYD6Jsh1VGZCtyYQmSro6APvN5Q62q1e4jV3fXuTK5WfCLx3W0FkHX6S3MWHZBu21x7U86T8BXfRiZCujEvJJEBnO8oluzxiJu5tcmAZDZD'}
    graph = facebook.GraphAPI(token)

    profile = graph.get_object('me', fields ='picture,events')

    profilePicture = profile['picture']['data']['url']
    storeProfilePictureLocally(profilePicture)
    
    return generateArrayOfEvents(events, profile)

def tkinter(events):
    #Set initial scale of the app
    HEIGHT = 750
    WIDTH = 480
    relYofEventCanvas = 0.1
    relHeightofEventCanvas = (HEIGHT / len(events)) / 1000
    #Initializing tkinter
    root = tk.Tk()

    mainCanvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#e9ebee')
    mainCanvas.pack()
    #Rendering the header for the app
    headerCanvas = tk.Canvas(mainCanvas, bg='#4267b2')
    headerCanvas.place(relx=0, rely=0, relheight=0.1, relwidth=1)

    headerFrame = tk.Frame(headerCanvas)
    headerFrame.place(relx=0.2, rely=0.2, relheight=0.6, relwidth=0.6)

    headerLabel = tk.Label(headerFrame, text='Upcoming events', font=("Courier", 15, 'bold'), bg='#4267b2', fg='white')
    headerLabel.place(relx=0, rely=0, relheight=1, relwidth=1)

    imageFrame = tk.Frame(headerCanvas, bg='blue')
    imageFrame.place(relx=0.02, rely=0.2, relheight=0.6, relwidth=0.1)

    image = ImageTk.PhotoImage(Image.open(r'images\ProfilePicture.png'))
    profile_photo = tk.Label(imageFrame, image=image)
    profile_photo.place(relx=0, rely=0, relheight=1, relwidth=1)

    for e in range(len(events)):
        eventTitle = '\n' + '\n' + events[e]['eventName'] + '\n' + '\n'
        eventStarts = 'Starts:  ' + events[e]['eventStarts']['date'] + '  klo ' + events[e]['eventStarts']['time']
        eventLocation = events[e]['eventPlace'].split(',')[0]
        keys = events[e].keys()
        eventStops = ''
        if 'endTime' in keys:
            eventStops = 'Ends:  ' + events[e]['endTime']
        else:
            eventStops = 'Ends:  ' + events[e]['eventEnds']['date'] + '  klo ' + events[e]['eventEnds']['time']
        
        eventTime = eventStarts + '\n' + eventStops
        
        eventCanvas = tk.Canvas(mainCanvas, bg='#1877f2')
        eventCanvas.place(relx=0, rely=relYofEventCanvas, relheight=0.18, relwidth=1)
        
        titleFrame = tk.Frame(eventCanvas, bg='#fff')
        titleFrame.place(relx=0.005, rely=0, relheight=0.15, relwidth=0.99)
        eventTitle = tk.Label(titleFrame, text=eventTitle, bg='#fff', font=("Courier", 11 , 'bold'), fg='#1877f2')
        eventTitle.place(relx=0, rely=0, relheight=1, relwidth=1)

        timeFrame = tk.Frame(eventCanvas, bg='#1877f2')
        timeFrame.place(relx=0.005, rely=0.15, relheight=0.28, relwidth=0.99)
        eventTime = tk.Label(timeFrame, text=eventTime, font=("Courier", 10), fg='white', bg='#1877f2')
        eventTime.place(relx=0, rely=0, relheight=1, relwidth=1)

        locationFrame = tk.Frame(eventCanvas, bg='#1877f2')
        locationFrame.place(relx=0.005, rely=0.4, relheight=0.57, relwidth=0.99)
        locationTitle = tk.Label(locationFrame, text='Location:\n', font=("Courier", 8), bg='#1877f2', fg='white')
        locationTitle.place(relx=0, rely=0.1, relheight=0.26, relwidth=1)
        eventLocationTitle = tk.Label(locationFrame, text=eventLocation, font=("Courier", 12),fg='white', bg='#1877f2')
        eventLocationTitle.place(relx=0, rely=0.2, relheight=0.38, relwidth=1)

        relYofEventCanvas = relYofEventCanvas + 0.125

    root.mainloop()

def main():
    events = []
    events = fetchFromGraphAPI(events)
    tkinter(events)

if __name__ == "__main__":
    main()