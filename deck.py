from random import shuffle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from csv import DictWriter

library_size = 99
library = []

def buildDeck(cards, lands, ramp):
    global library
    library = []
    land_count = 0
    ramp_count = 0
    for x in range(cards):
        if land_count < lands:
            library.append(1)
            land_count += 1
        elif ramp_count < ramp:
            library.append(2)
            ramp_count += 1
        else:
            library.append(0)

def drawHand(amount):
    global library
    buildDeck(library_size, land_amount, ramp_amount)
    shuffle(library)
    hand = []
    for x in range(amount):
        hand.append(library[0])
        library.pop(0)
    return hand

def checkHand():
    global library
    next_mulligan = 8

    hand = drawHand(7)

    while True:
        if (hand.count(1) < 3 or hand.count(1) > 4) and next_mulligan > 7:
            next_mulligan -= 1
            hand = drawHand(next_mulligan)

        elif (hand.count(1) < 3 or hand.count(1) > 5) and next_mulligan > 6:
            next_mulligan -= 1
            hand = drawHand(next_mulligan)

        elif (hand.count(1) < 2 or hand.count(1) > 5) and next_mulligan > 5:
            next_mulligan -= 1
            hand = drawHand(next_mulligan)
        elif (hand.count(1) == 0 or hand.count(1) == 5) and next_mulligan > 4:
            next_mulligan -= 1
            hand = drawHand(next_mulligan)

        else:
            break
    return hand

def simulateHands(amount):
    global library
    screwed = 0
    flooded = 0
    good = 0
    for x in range(amount):
        hand = checkHand()
        for x in range(4+expected_drawn):
            hand.append(library[0])
            library.pop(0)
        if hand.count(1)/len(hand) > 0.5 or (hand.count(1) + hand.count(2))/len(hand) > 0.80:
            flooded += 1
        elif hand.count(1) + hand.count(2) < 4:
            screwed += 1
        else:
            good += 1

    print(f'Simulations: {sim_num}')
    print(f'Lands: {land_amount}\tRamp: {ramp_amount}\t Extra Draw: {expected_drawn}')
    print(f'Good: {"{:.2f}".format((good / amount) * 100)}%')
    print(f'Flooded: {"{:.2f}".format((flooded / amount) * 100)}%')
    print(f'Screwed: {"{:.2f}".format((screwed / amount) * 100)}%\n')

decks = pd.read_csv('DeckAverages.csv')
X = decks.drop(columns=['lands'])
Y = decks['lands']

model = DecisionTreeClassifier()
model.fit(X.values, Y.values)

calculate_deck_lands = input('Would you like us to calculate the suggested amount of lands in your deck? Type y or n: ')

while True:
    if calculate_deck_lands.lower() == 'y':
        avg_mana = input('What is the average mana cost of your deck?: ')
        while True:
            try:
                avg_mana = float(avg_mana)
                break
            except:
                avg_mana = input('That was not a valid response, what is the average mana cost of your deck: ')

        suggested_lands = model.predict([[avg_mana]])[0]
        print(f'The suggested amount of lands is {suggested_lands}\n')
        land_amount = suggested_lands
        break
    elif calculate_deck_lands.lower() == 'n':
        land_amount = input('How many lands are in your deck?: ')
        while True:
            try:
                land_amount = int(land_amount)
                break
            except:
                land_amount = input('That is not a valid number, how many lands are in your deck: ')
        break
    else:
        calculate_deck_lands = input('That was not a valid response, would you like us to calculate the suggested '
                                     'amount of lands in your deck? Type y or n: ')

expected_drawn = input('\nHow many cards do you expect to draw by turn 4(excluding normal draw step): ')
while True:
    try:
        expected_drawn = int(expected_drawn)
        break
    except:
        expected_drawn = input('That was not a valid number, how many cards do you expect to draw by turn 4: ')

ramp_amount = input('\nHow many sources of ramp do you have in the deck?: ')
while True:
    try:
        ramp_amount = int(ramp_amount)
        break
    except:
        ramp_amount = input('That was not a valid number, how many sources of of ramp do you have in the deck: ')

sim_num = input('\nHow many times would you like to run the simulation?: ')
while True:
    try:
        sim_num = int(sim_num)
        break
    except:
        sim_num = input('That was not a valid number, how many times would you like to run the simulation: ')

print()
simulateHands(sim_num)

add_deck_data = input('Would you like to add data to help our machine make better land suggestions? Type y or n: ')
while True:
    if add_deck_data.lower() == 'y':
        add_lands = input('\nHow many lands are in your deck?: ')
        while True:
            try:
                add_lands = int(add_lands)
                break
            except:
                add_lands = input('That is not a valid number, how many lands are in your deck: ')

        add_mana_avg = input('What is the average mana cost of your deck?: ')
        while True:
            try:
                add_mana_avg = "{:.1f}".format(float(add_mana_avg))
                break
            except:
                add_mana_avg = input('That was not a valid number, what is the average mana cost of your deck: ')

        file = open('DeckAverages.csv', 'a')
        add_data = {'lands': add_lands, 'avg_mana_cost': add_mana_avg}
        DictWriter(file, ['lands', 'avg_mana_cost']).writerow(add_data)
        print('\nThank you for adding your data to our system, your help is much appreciated!')
        file.close()
        break

