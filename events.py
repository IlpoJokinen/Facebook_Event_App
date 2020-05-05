import tkinter as tk
import facebook
import pybase64
import urllib
import json
from PIL import ImageTk, Image
import datetime as dt

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

def fetchFromGraphAPI(event):
    token = {'EAAJyBpwkDxMBAPya4bkoyRWZAdHXlniaaXDbIfwwiWBh30yYg5cf0y5yoR46GtYIW9rZBOkT61spVjpj4pv4te6ffzc2iZAJW6HyPsFmp08gbcmg3xFx9Uql1LC64PGMME1fRd9grKcXm7nlsoeLIW3HSPtqubYnyGszvkAJtZCUUTnXdNNodoZAE052ycYALqj6tPXN1uAZDZD'}
    graph = facebook.GraphAPI(token)

    profile = graph.get_object('me', fields ='picture,events')

    profilePicture = profile['picture']['data']['url']
    storeProfilePictureLocally(profilePicture)
    try:
        cut = slice(-8)
        #print(json.dumps(profile, indent=4))
        event = {
            'eventName': profile['events']['data'][0]['name'],
            'eventPlace': profile['events']['data'][0]['place']['name'],
            'startTime': profile['events']['data'][0]['start_time'][cut],
            'endTime': profile['events']['data'][0]['end_time'][cut]
        }
        eventStarts = formatEventDateTime(event['startTime'])
        eventEnds = formatEventDateTime(event['endTime'])
        event.update([('eventStarts', eventStarts), ('eventEnds', eventEnds)])
        del event['startTime']
        del event['endTime']
    except UnicodeEncodeError:
        print('There was an error encoding the facebook event!')  

    return event 
    
def tkinter(event):
    print(event)
    #Getting the data from facebook profile
    #fetchFromGraphAPI()
    #Set initial scale of the app
    HEIGHT = 600
    WIDTH = 350
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

    eventFrame1 = tk.Frame(root, bg='#007599')
    eventFrame1.place(relx=0, rely=0.08, relheight=0.19, relwidth=1)

    eventTitle = tk.Label(eventFrame1, text=event['eventName'], bg='#007599')
    eventTitle.place(relheight=0.5, relwidth=1)
    
    root.mainloop()

def main():
    event = {}
    event = fetchFromGraphAPI(event)
    tkinter(event)

if __name__ == "__main__":
    main()
