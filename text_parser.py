import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

r = re.compile('^([0-9]*)x.*')

def prompt_for_txt():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return filename

def get_card_names():
    cardList = []
    filename = prompt_for_txt()

    if filename == '':
        return
    
    with open(filename, encoding='utf8') as f:
            for line in f:
                #account for quantity
                if r.match(line) is not None:
                    #split into tuple and store card quantity/name
                    splitCard = line.split("x", 1)
                    cardQuantity = int(splitCard[0])
                    cardName = splitCard[1].strip()
                    cardList.append((cardQuantity, cardName))
                else:
                    #default to one cardQuantity
                    cardList.append((1, line.strip()))
    return cardList


def print_cardlist():
    for card in get_card_names():
        print(card)

