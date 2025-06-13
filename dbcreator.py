# importing csv module
import csv
import sqlite3

# csv file name
filename = "units.csv"
csvs = ["units.csv", "units.csv", "cards.csv", "cards.csv", "spells.csv"]
#csvs = ["units.csv", "cards.csv"]#, "spells.csv"]

# initializing the titles and rows list
fields = []
rows = []

# list of tables
list_tables = ["units_a", "units_b", "cards_a", "cards_b", "spells"]
#list_tables = ["units", "cards"]#, "spells"]
def csvlistconverter(filename):
# csv file name
    

# initializing the titles and rows list
    fields = []
    rows = []

    # reading csv file
    with open(filename, "r") as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

        
    
    return fields, rows

def cardextraction(cardsroute):
    decki = []
    
    notcare, individual = csvlistconverter(cardsroute)
    for cd in individual:
        if cd[2] != "":
            cou = cd[2]
            cd.pop(2)
            for num in range(int(cou)):
                
                name = cd[0]+str(num)
                temp = cd[1:]
                temp.insert(0,name)
                decki.append(temp)
                
                
        else:
            cd.pop(2)
            decki.append(cd)
    
    
                
    return decki

def repeated_token_extraction(tokenlist):
    
    token_out = []
    for token in tokenlist:
        
        for nr in range(int(token[1])):
            name = token[0]+str(nr)
            temp = token[2:]
            temp.insert(0,name)
            token_out.append(temp)
    return token_out


def conection_sql():
    global conector
    conector = sqlite3.connect("currentgame.db")
    return conector

def tabledropper(conection, table):
    pointer = conection.cursor()
    dropping = "DROP TABLE IF EXISTS "+table 
    pointer.execute(dropping)
    conection.commit()
    

    

def tableconstructor(conection):
    pointer = conection.cursor()
    table = "CREATE TABLE IF NOT EXISTS deck(id INTEGER PRIMARY KEY AUTOINCREMENT, card TEXT NOT NULL, type TEXT NOT NULL, income INTEGER, power INTEGER,  agrogen INTEGER,  defenders INTEGER, mining INTEGER, refinerie INTEGER, colonies INTEGER, labs INTEGER, notes TEXT, force INTEGER, hits INTEGER, placement TEXT, deckpos INTEGER, hitted INTEGER  )"
    pointer.execute(table)
    conection.commit()
    tableimages = "CREATE TABLE IF NOT EXISTS images(id INTEGER PRIMARY KEY AUTOINCREMENT, card TEXT NOT NULL, pict TEXT, descript TEXT )"
    pointer.execute(tableimages)
    conection.commit()
    
def tableconstructor(conection, fields, table_name,selection = None, ):
    
    try:
        fields.remove("Nbr")
    except: pass
    pointer = conection.cursor()
    table = "CREATE TABLE IF NOT EXISTS "+table_name+"(id INTEGER PRIMARY KEY AUTOINCREMENT, %s TEXT )" % " TEXT, ".join(fields)
    
    
    pointer.execute(table)
    conection.commit()
    


def alltablesconstructor(conection, faction_a, faction_b):
    
    for ind in range(len(csvs)):
        fields, rows = csvlistconverter(csvs[ind])
        try:
            fields.remove("Nbr")
            rows =repeated_token_extraction(rows)
        except: pass
        pointer = conection.cursor()
        table = "CREATE TABLE IF NOT EXISTS "+list_tables[ind]+"(id INTEGER PRIMARY KEY AUTOINCREMENT, %s TEXT )" % " TEXT, ".join(fields)
        
        pointer.execute(table)
        conection.commit()
        
        for row in rows:
            
            preload = "INSERT INTO "+list_tables[ind]+"(%s) VALUES (" % ",".join(fields)
            
            preload = preload + "?,"*len(fields)
            preload = preload[:-1]
            preload =  preload + ")"
            #preload3 = preload + " WHERE Faction = "+ str(faction_a) + " GROUP BY Faction;" 
            #print(preload3)
            
            preload2 = []
            for discrete in row:
                preload2.append(str(discrete))
            
            tupleload = tuple(preload2)
            
            pointer.execute(preload, tupleload)
            conection.commit()
        #tableconstructor(conection, fields, list_tables[ind])
        
# Opcion con filtrado

def alltablesconstructor(faction_list):
    
    
    conector = conection_sql()
    for ind in range(len(list_tables)):
        tabledropper(conector, list_tables[ind])
        individual_table(conector, csvs[ind], list_tables[ind],faction_list[ind%2])
    
    

def individual_table(conection, csv, table_to_create, faction = "None"):
    
    fields, rows = csvlistconverter(csv)
    try: 
        fields.remove("Nbr")
        rows = repeated_token_extraction(rows)
    except: pass
    
    faction_rows = []
    try:
        faction_field_index = fields.index("Faction")
    
        for row in rows:
            if row[faction_field_index] == faction:
                faction_rows.append(row)
    except: faction_rows = rows.copy()
    #print(faction_field_index)
    
    
    pointer = conection.cursor()
    table = "CREATE TABLE IF NOT EXISTS "+table_to_create+"(id INTEGER PRIMARY KEY AUTOINCREMENT, %s TEXT )" % " TEXT, ".join(fields)
    
    pointer.execute(table)
    conection.commit() 
    
    for row in faction_rows:
            
        preload = "INSERT INTO "+table_to_create+"(%s) VALUES (" % ",".join(fields)
        
        preload = preload + "?,"*len(fields)
        preload = preload[:-1]
        preload =  preload + ")"
        
        
        preload2 = []
        for discrete in row:
            preload2.append(str(discrete))
        
        tupleload = tuple(preload2)
        
        pointer.execute(preload, tupleload)
        conection.commit()       

def loaddb(coneccion, tuplacarga):

    

    pointer = coneccion.cursor()
    carga = "INSERT INTO deck(card, type, income, power, agrogen, defenders, mining, refinerie, colonies, labs, notes, force, hits, placement, deckpos, hitted) VALUES (?,?,?,?,?,?,?,?,?,?, ?,?,?,?,?,?)"
    pointer.execute(carga, tuplacarga)
    coneccion.commit()
    
    
def loadimages(coneccion, tupleimages):
    
    pointer = coneccion.cursor()
    load = "INSERT INTO images(card, pict, descript) VALUES (?,?,?)"
    pointer.execute(load, tupleimages)
    coneccion.commit()
    

def massiveloader(conector, deck):
    for x in deck:
        row = x
        
        income = int(row[2])
        power = int(row[3])
        agrogen = int(row[4])
        defenders = int(row[5])
        mining = int(row[6])
        refinerie = int(row[7])
        colonies = int(row[8])
        labs = int(row[9])
        force = int(row[11])
        hits = int(row[12])
        loadtuple = (row[0], row[1], income, power, agrogen, defenders, mining, refinerie, colonies, labs, row[10], force, hits, row[13], row[14], row[15])
        
        loaddb(conector, loadtuple)
        
        loadimagestuple = (row[0], row[16], row[17])
        loadimages(conector, loadimagestuple)

def data_loader(conection, rows, fields):
    
    pointer = conection.cursor
    for row in rows:
        load_tuple = tuple(row)
        
        
    pass    

def individual_list(csv, faction = "None"):
    
    fields, rows = csvlistconverter(csv)
    try: 
        fields.remove("Nbr")
        rows = repeated_token_extraction(rows)
    except: pass
    #rows = repeated_token_extraction(rows)
    
    faction_rows = []
    try:
        faction_field_index = fields.index("Faction")
    
        for row in rows:
            if row[faction_field_index] == faction:
                faction_rows.append(row)
    except: faction_rows = rows.copy()
    return fields, faction_rows



def main(faction_list):
    
    #alltablesconstructor(faction_list)
    
    print(individual_list(csvs[4]))

if __name__ == "__main__":
    factions = ["DEEP_ONES", "CULTIST"]
    main("k")
    
    
    
    
    
        
    
    
    
    


    

    


