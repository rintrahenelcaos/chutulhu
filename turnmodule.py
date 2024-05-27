import sqlite3
import random



def conection_sql():
    global conector
    conector = sqlite3.connect("currentgame.db")
    return conector

def deckmixer(db):
    
    to_shuffle = []
    
    pointer = conector.cursor()
    
    extractor = "SELECT id FROM "+db
    pointer.execute(extractor)
    cards = pointer.fetchall()
    
    for card in cards:
        to_shuffle.append(card[0])
    random.shuffle(to_shuffle)
    
    for position in range(len(to_shuffle)):
        
        positioner = "UPDATE "+db+" SET Deckorder=? WHERE id=?"
        tupleloader = (to_shuffle[position], position+1)
        
        pointer.execute(positioner, tupleloader)
        conector.commit()
    return to_shuffle

def deck_assigner(db):
    
    pointer = conector.cursor()
    
    idcount = "SELECT MAX(id) FROM "+db
    pointer.execute(idcount)
    cardcount = pointer.fetchall()[0][0]+1
    print(cardcount)
    
    for i in range(cardcount):
        
        to_deck = "UPDATE "+db+" SET Location = ? WHERE id=?"
        
        pointer.execute(to_deck, ("deck", str(i+1)))
        conector.commit()

def drawer(db):
    
    pointer = conector.cursor()
    
    top_of_deck = "SELECT MIN(Deckorder)"
    

def fate_phase():
    
    pointer = conector.cursor()
    

def main():
    conector = conection_sql()
    print(deckmixer("cards_a"))
    deck_assigner("cards_a")
    
if __name__ == "__main__":
    
    main()
    