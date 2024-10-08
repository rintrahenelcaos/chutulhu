
import sqlite3
import random
from dbcreator import conection_sql


"""def conection_sql():
    global conector
    conector = sqlite3.connect("currentgame.db")
    return conector"""

# DB intermediate functions

def deckmixer(db):
    
    to_shuffle = []
    conector = conection_sql()
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
    
    conector = conection_sql()
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
    
    conector = conection_sql()
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
    
def discarder(db, card):
    
    conector = conection_sql()
    pointer = conector.cursor()
    
    to_discard = "UPDATE "+db+" SET location='discard' WHERE Card_Name='"+card+"'"
    
    pointer.execute(to_discard)
    conector.commit()
    
def reshuffle_deck(db):    
    
    conector = conection_sql()
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
    
def card_counter(db, deck):
    
    conector = conection_sql()
    pointer = conector.cursor()
    
    deckcounter = "SELECT COUNT(*) FROM "+db+" WHERE location='"+deck+"'"
    print(deckcounter)
    pointer.execute(deckcounter)
    deckcount = pointer.fetchone()[0]
    print("deckcount = ", deckcount, " ", type(deckcount))
    
    return deckcount

def card_data_extractor(db, deck, data = "Card_Name,Type,Range,Notes,Images"):
    
    conector = conection_sql()
    pointer = conector.cursor()
    
    hand_list = []
    try:
        to_get = "SELECT "+data+" FROM "+db+" WHERE location ='"+deck+"'"
        print(to_get)
        pointer.execute(to_get)
    except:
        to_get = "SELECT "+data+" FROM "+db+" WHERE location ='"+deck+"'"
        print(to_get)
        pointer.execute(to_get)
    hand_list = pointer.fetchall()
    print("hand_list: ",hand_list)
    
    return hand_list

def token_extractor(data):
    
    conector = conection_sql()
    pointer = conector.cursor()
    
    token_list = []
    
    tokens_info = "SELECT Images,Unit_name,hits,notes from "+data+";"
    pointer.execute(tokens_info)
    token_list = pointer.fetchall()
    print(token_list)
    return token_list
    

if __name__ == "__main__":
    
    token_extractor("units_a")