import tkinter as tk
from PIL import ImageTk, Image

def tkinter(events):
    #Set initial scale of the app
    HEIGHT = 750
    WIDTH = 480
    relYofEventCanvas = 0.1
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

    #Looping the events array and making a frame of each of the events in to the canvas.
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