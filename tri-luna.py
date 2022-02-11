import sys
import requests
import json
import random

# Command Line error handling
if len(sys.argv) < 3:
    raise Exception("You have not provided enough arguments\nThis script should be run like: 'python3 deck.ydk 100'")
elif len(sys.argv) > 3:
    raise Exception("You have provided too many arguments\nThis script should be run like: 'python3 deck.ydk 100'")
elif sys.argv[1][-4:] != '.ydk':
    raise Exception("Provided decklist is not a .ydk file!")
elif not (isinstance(int(sys.argv[2]), int)):
    raise Exception("Loop amount is not a positive integer!")

class Calculator:
    def __init__(self):
        # Stats tracked
        self.loopAmount = int(sys.argv[2])
        self.fullCombo = 0
        self.fullCombo2Nerv = 0
        self.smallWorldUsedForCombo = 0

        with open(sys.argv[1]) as f:
            deck_ids = f.read().splitlines()
        deck_ids.pop(0)
        deck_ids.pop(0)
        self.decksize = deck_ids.index("#extra")
        deck_ids = deck_ids[:self.decksize]
        deck = []
        # Convert card ids to names
        for card in deck_ids:
            response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
            info = json.loads(response.text)
            name = info["data"][0]["name"]
            deck.append(name)
        self.deck  = deck

    def checkHand(self, hand):
        if "Lunalight Kaleido Chick" in hand:
            if "Lunalight Tiger" in hand:
                self.fullCombo += 1
                return
            elif "Luna Light Perfume" in hand:
                self.fullCombo += 1
                return
            elif "Tri-Brigade Fraktall" in hand:
                self.fullCombo += 1
                return
            elif "Foolish Burial Goods" in hand:
                self.fullCombo += 1
                return
            elif "Small World" in hand:
                # Check if targets for Small World are in hand instead
                # TODO: check other hand traps if they work for this
                if "Ash Blossom & Joyous Spring" in hand or "Armageddon Knight" in hand:
                    self.fullCombo += 1
                    self.smallWorldUsedForCombo += 1
                    return
                elif "Tri-Brigade Nervall" in hand:
                    self.fullCombo += 1
                    self.fullCombo2Nerv += 1
                    self.smallWorldUsedForCombo += 1
                    return 
        if "Tri-Brigade Fraktall" in hand:
            if "Luna Light Perfume" in hand:
                self.fullCombo += 1
                return
            elif hand.count("Tri-Brigade Fraktall") >= 2 or "Tri-Brigade Nervall" in hand or "Tri-Brigade Kitt" in hand or "Lunalight Yellow Marten" in hand:
                self.fullCombo += 1
                return
            elif "Small World" in hand:
                if "Ash Blossom & Joyous Spring" in hand:
                    self.fullCombo += 1
                    self.smallWorldUsedForCombo += 1
                    return
                if "Ghost Ogre & Snow Rabbit" in hand:
                    self.fullCombo += 1
                    self.fullCombo2Nerv += 1
                    self.smallWorldUsedForCombo += 1
                    return

        if "Foolish Burial" in hand:
            if "Foolish Burial Goods" in hand:
                self.fullCombo += 1
                return
            elif "Luna Light Perfume" in hand:
                self.fullCombo += 1
                return
        if "Foolish Burial Goods" in hand and "Lunalight Serenade Dance" in hand:
            self.fullCombo +=1
            return
        if "Armageddon Knight" in hand or "Reinforcement of the Army" in hand:
            if "Luna Light Perfume" in hand:
                self.fullCombo += 1
                return
            

    def run(self):
        # Combo Logic
        for i in range(self.loopAmount):
            random.shuffle(self.deck)
            hand = self.deck[-5:]

            # Check hands
            self.checkHand(hand)

        # Print Stats
        print("Total percent Boards finishing on full board:")
        print((self.fullCombo / self.loopAmount) * 100)
        print("Percent Boards finishing on full board only if you play 2 Nervall:")
        print((self.fullCombo2Nerv / self.loopAmount) * 100)
        print("Percent Boards finishing on full board only if you play Small World:")
        print((self.smallWorldUsedForCombo / self.loopAmount) * 100)

test = Calculator()
test.run()
