
import sqlite3
import random


def conection_sql():
    global conector
    conector = sqlite3.connect("currentgame.db")
    return conector

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