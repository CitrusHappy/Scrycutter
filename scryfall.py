import text_parser
import requests
import ujson
import os
from shutil import copyfileobj
from datetime import datetime as dt


bulkDataFileName = 'bulkdata.json'
imagesDirectory = 'Card Images'

if not os.path.exists(imagesDirectory):
    os.makedirs(imagesDirectory)

def batch_image_download(cardList):
    for cardTuple in cardList:
        #check for dupes here, and continue(skip) if it is already downloaded
        card = cardTuple[1]
        sameCards = []
        print('Searching for card ' + card)

        with open(bulkDataFileName, encoding="utf8") as bulkJson:
            bulkData = ujson.load(bulkJson)
    
        # Get the image URL
        for i in bulkData:
            if i['name'] == card:
                if i['lang'] == 'en':
                    if i['set'] != 'prm' and i['promo'] == False and i['border_color'] == 'black' and i['set'] != 'akr':
                        sameCards.append(i)
                            
        
        print(str(len(sameCards)) + ' version(s) of ' + card + ' were found.')
        if len(sameCards) > 0:
            newestCard = max(sameCards, key=lambda ev: dt.strptime(ev['released_at'], "%Y-%m-%d"))

            imgUrl = newestCard['image_uris']['png']

            #save the current sheet
            with open(imagesDirectory +'/'+ card +'.png', 'wb') as out_file:
                copyfileobj(requests.get(imgUrl, stream = True).raw, out_file)
        else:
            print(card + ' not found, is it misspelled?')
            

def clean_images():
    for file in os.scandir(imagesDirectory):
        os.remove(file)


def bulk_data_fetch():
    api = requests.get('https://api.scryfall.com/bulk-data')
    apiJson = api.json()

    bulkDataUrl = apiJson['data'][2]['download_uri']
    response = requests.get(bulkDataUrl)

    with open(bulkDataFileName, 'wb') as out_file:
        out_file.write(response.content)
    