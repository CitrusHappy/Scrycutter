import numpy as np
import os
import math
import PIL
import text_parser
from PIL import Image
from scryfall import imagesDirectory


sheetsDirectory = 'Sheets/'
offset = 68

if not os.path.exists(sheetsDirectory):
    os.makedirs(sheetsDirectory)

def combine_images(cardList):
    cardImages = []

    #create list of card images
    for cardTuple in cardList:
        path = imagesDirectory + '/' + cardTuple[1] + '.png'

        #skip over cards that have no images
        if not os.path.exists(path):
            continue

        cardImage = Image.open(path)
        cardImage = cardImage.resize((745, 1040), PIL.Image.Resampling.BICUBIC)
        for i in range(0 , cardTuple[0], 1):
            cardImages.append(cardImage)


    #split into sheets of 9
    sheetCount = math.ceil(len(cardImages)/9)
    print(str(sheetCount) + ' sheet(s) will be produced.')

    for m in range(0, sheetCount, 1):
        canvas = Image.new(mode='RGB', size=(2550, 3300), color=(255,255,255))

        for t in range(offset,2235+offset,765):
            for g in range(offset,3120+offset,1060):
                #paste the image at location i,j:
                if(len(cardImages) != 0):
                    canvas.paste(cardImages.pop(), (t,g))

        #canvas.show()
        canvas.save(sheetsDirectory + 'sheet' + str(m+1) + '.png', resolution=300)


def clean_sheets():
    for file in os.scandir(sheetsDirectory):
        os.remove(file)