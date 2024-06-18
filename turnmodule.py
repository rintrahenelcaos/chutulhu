import sqlite3
import random



def conection_sql():
    global conector
    conector = sqlite3.connect("currentgame.db")
    return conector

def deckmixer(db):
    
    to_shuffle = []
    
    pointer = conector.cursor()
    
    extractor = "SELECT id FROM "+db+" WHERE location='deck'"
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

def drawer(db, player_hand, origin):
    
    pointer = conector.cursor()
    
    deck_order = "SELECT Deckorder FROM "+db+" WHERE location='"+origin+"'"
    print(deck_order)
    
    pointer.execute(deck_order)
    order = pointer.fetchall()
    list_order = []
    for ord in order:
        lst = list(ord)
        lst[0] = int(lst[0])
        list_order.append(lst[0])
    
    min_order = min(list_order)
    
    
    to_hand = "UPDATE "+db+" SET location='"+player_hand+"' WHERE Deckorder="+str(min_order)
    
    
    pointer.execute(to_hand)
    conector.commit()
    
    """clear_deckorder = "UPDATE "+db+" SET Deckorder='' WHERE Deckorder="+str(min_order)
    
    pointer.execute(clear_deckorder)
    conector.commit()"""
    
def reshuffle_deck(db):    
    
    pointer = conector.cursor()
    
    """idcounter = "SELECT id FROM "+db+" WHERE location='hand'"
    pointer.execute(idcounter)
    idcount = pointer.fetchall()
    
    print(idcount)
    
    idstuple = tuple([i[0] for i in idcount])
    
    print(idstuple)
    
    
    changer = "UPDATE "+db+" SET location='deckn' WHERE id IN "+str(idstuple)"""
    changer = "UPDATE '"+db+"' SET location='deck' WHERE location='discard'"
    pointer.execute(changer)
    conector.commit()
        
        
        

def fate_phase(db, deck, player):
       
    """Draw 3 cards from your deck. 
    Max hand size = 5 cards.
    If the deck runs out, shuffle the discard and draw from it.
    Discard excess cards."""
    
    pointer = conector.cursor()
    
    for i in range(3):
        deckcounter = "SELECT COUNT(*) FROM "+db+" WHERE location='"+deck+"'"
        print(deckcounter)
        pointer.execute(deckcounter)
        deckcount = pointer.fetchone()[0]
        print("deckcount = ", deckcount, " ", type(deckcount))
        
        if deckcount == 0:
            
            reshuffle_deck(db)
            deckmixer(db)
            print("reshufle")
            
        drawer(db,player, deck)    
    #drawer(deck, player)
    

def main():
    conector = conection_sql()
    #print(deckmixer("spells"))
    #deck_assigner("spells")
    pointer = conector.cursor()
    changer = "UPDATE spells SET location='discard'"
    pointer.execute(changer)
    conector.commit()
    reshuffle_deck("spells")
    deckmixer("spells")
    
    idcount = "SELECT MAX(id) FROM spells"
    pointer.execute(idcount)
    cardcount = pointer.fetchall()[0][0]
    print(cardcount)
    
    for i in range(cardcount):
        print(i)
        #drawer("spells", "discard")
        fate_phase("spells", 'deck',"discard")
        #drawer("spells", "discard", "deck")
        print(i)
        
        
    
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #reshuffle_deck("spells")
    
    
    
if __name__ == "__main__":
    
    main()
    