import os.path
import datetime
import text_parser
import image_combiner
import scryfall
import tkinter as tk
from tkinter import ttk

def scrycutter():
    bulkDataFileName = 'bulkdata.json'
    
    if os.path.exists(bulkDataFileName):
        today = datetime.datetime.today()
        bulk_data_age = datetime.datetime.fromtimestamp(os.path.getmtime(bulkDataFileName))
        age = today - bulk_data_age
        if age.days > 7:
            print('Bulk data old, fetching new data.')
            os.remove(bulkDataFileName)
            scryfall.bulk_data_fetch()
        else:
            print('Bulk data OK')
    else:
        print('Bulk data does not exist, fetching new data.')
        scryfall.bulk_data_fetch()

    cardList = text_parser.get_card_names()

    scryfall.clean_images()
    scryfall.batch_image_download(cardList)

    image_combiner.clean_sheets()
    image_combiner.combine_images(cardList)
    print('Finished!')
    text.set("Finished cutting!")



#this is messy but im running out of time
root = tk.Tk()
root.title('Scrycutter')
#root.iconbitmap('icon.ico')

# Initialize style
s = ttk.Style()
# Create style used by default for all Frames
s.configure('TFrame', background='#242424')
s.configure('Text.White', foreground='#ffffff', background='#242424')

frm = ttk.Frame(root, padding=50, style='TFrame')
frm.grid()

text = tk.StringVar()
text.set('Choose a text file to start cutting!')
ttk.Label(frm, textvariable=text, font=('Helvetica', 11)).grid(column=0, row=0)
ttk.Button(frm, text="Select card list text file", command=scrycutter, padding=5).grid(column=0, row=1)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=2)

root.mainloop()


