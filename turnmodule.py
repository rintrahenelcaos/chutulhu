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
        
        to_deck = "UPDATE "+db+" SET location = ? WHERE id=?"
        print(to_deck)
        pointer.execute(to_deck, ("deck", str(i+1)))
        conector.commit()

def drawer(db):
    
    pointer = conector.cursor()
    
    deck_order = "SELECT Deckorder FROM "+db+" WHERE location='deck'"
    print(deck_order)
    
    pointer.execute(deck_order)
    order = pointer.fetchall()
    list_order = []
    for ord in order:
        lst = list(ord)
        lst[0] = int(lst[0])
        list_order.append(lst[0])
    
    min_order = min(list_order)
    
    
    to_hand = "UPDATE "+db+" SET location='hand' WHERE Deckorder="+str(min_order)
    
    
    pointer.execute(to_hand)
    conector.commit()
    
    clear_deckorder = "UPDATE "+db+" SET Deckorder='' WHERE Deckorder="+str(min_order)
    
    pointer.execute(clear_deckorder)
    conector.commit()
    
def reshuffle_deck(db):    
    
    pointer = conector.cursor()
    
    idcounter = "SELECT id FROM "+db+" WHERE location='hand'"
    pointer.execute(idcounter)
    idcount = pointer.fetchall()
    
    print(idcount)
    
    idstuple = tuple([i[0] for i in idcount])
    
    print(idstuple)
    
    changer = "UPDATE "+db+" SET location='deckn' WHERE id IN "+str(idstuple)
    
    pointer.execute(changer)
    conector.commit()
        
        
        

def fate_phase():
    
    pointer = conector.cursor()
    

def main():
    conector = conection_sql()
    print(deckmixer("spells"))
    deck_assigner("spells")
    """pointer = conector.cursor()
    changer = "UPDATE spells SET location='discard'"
    pointer.execute(changer)
    conector.commit()"""
    drawer("spells")
    drawer("spells")
    drawer("spells")
    reshuffle_deck("spells")
    
    
if __name__ == "__main__":
    
    main()
    