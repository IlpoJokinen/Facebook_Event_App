import tkinter as tk
import facebook
import pybase64
import urllib
import json
from PIL import ImageTk, Image
import datetime as dt
from operator import attrgetter

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
    token = {'EAAJyBpwkDxMBAJFu7XLn7z1v9QjTXwCDZClTx8oLXlaO9twHXZAUECWxGVOPNgdtJFEQi5SseGQknrZB0RmGDLa5n4sejIuwNT7mxAV1ZCZCugjwO0WllMHsAMtf4kQ7OpCBYmdQ5kHf4JZCWBausgfgUGRnwr8ZBgptyprHMmHtQc5ZA7sOTmwVI8qIhZCx03THtu3p5etE5PiQWjTB7EajV8OpG06wOPriXSdSVuEAo4wZDZD'}
    graph = facebook.GraphAPI(token)

    profile = graph.get_object('me', fields ='picture,events')

    profilePicture = profile['picture']['data']['url']
    storeProfilePictureLocally(profilePicture)
    
    return generateArrayOfEvents(events, profile)

def tkinter(events):
    #print(events)
    #Set initial scale of the app
    HEIGHT = 600
    WIDTH = 350
    heightOfEventFrame = (HEIGHT / len(events)) / 1000
    relYofEventFrame = 0.08
    print(heightOfEventFrame)
    #Initializing tkinter
    root = tk.Tk()

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()
    #Rendering the header for the app
    headerFrame = tk.Frame(root, bg='#e6f9ff')
    headerFrame.place(relx=0, rely=0, relheight=0.08, relwidth=1)

    headerLabel = tk.Label(headerFrame, text='Upcoming events', bg='#e6f9ff')
    headerLabel.place(relx=0.38, rely=0.26)
    image = ImageTk.PhotoImage(Image.open(r'images\ProfilePicture.png'))

    profile_photo = tk.Label(headerFrame, image=image)
    profile_photo.place(relheight=1, relwidth=0.15)

    for e in range(len(events)):
        eventFrame = tk.Frame(root, bg='#007599')
        eventFrame.place(relx=0, rely=relYofEventFrame, relheight=heightOfEventFrame, relwidth=1)

        eventTitle = tk.Label(eventFrame, text=events[e]['eventName'], bg='#007599')
        eventTitle.place(relheight=0.5, relwidth=1)

        relYofEventFrame = relYofEventFrame + 0.077
    
    root.mainloop()

def main():
    events = []
    events = fetchFromGraphAPI(events)
    tkinter(events)

if __name__ == "__main__":
    main()