import sqlite3



def conection_sql():
    global conector
    conector = sqlite3.connect("currentgame.db")
    return conector



def fate_phase():
    
    pointer = conector.cursor()
    