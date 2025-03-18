
def recv_msg_translator(cargo):
    
    if cargo != "NONE":
    
        first_split = cargo.rsplit("]")
        code = first_split[0]
        second_split = first_split[1].rsplit(":")
        target = second_split[0]
        order = second_split[1]
        if code == "BATCH":  # initial deploy order. Structure: "BATCH]all:xpos1,ypos1;xpos2,ypos;..."
            print("initial deploy")
            coordinates = order.rsplit(";")
            order = []
            for coord in coordinates:
                individual = coord.rsplit(",")
                xpos = float(individual[0])
                ypos = float(individual[1])
                coord_tuple = (xpos, ypos)
                order.append((coord_tuple))
        elif code == "VECTORTOGO":
            print("move token")
            coordinates = order.rsplit(",")
            order = []
            xpos = float(coordinates[0])
            ypos = float(coordinates[1])
            coord_tuple = (xpos, ypos)
            order.append((coord_tuple))
        elif code == "CARDSDRAWN":
            cards_list = order.rsplit(";")
            order = []
            for card in cards_list:
                order.append(card)
            print("cards drawn")
        elif code == "CARDPLAYED":
            
            
            print("card played")
        elif code == "DAMAGE":
            print("damage dealt to token")
            order = int(order) 
        elif code == "DEFENSE":
            print("defense activated")
            order = int(order)   
        
        elif code == "ACARDPLAYED":
            print("move token")
        elif code == "XCARDPLAYED":
            print("move token")
        elif code == "SCARDPLAYED":
            print("move token")


        print("recv_msg_translator: ---> " + cargo)
        return code, target, order
    
    
    

def send_msg_translator(code, target, order):
    
    if code == "VECTORTOGO":
        orderx = order[0]
        ordery = order[1]
        send_msg = code+"]"+str(target)+":"+str(orderx)+","+str(ordery)
    elif code == "CARDSDRAWN":
        temporal_order = ""
        for ind_order in order:
            temporal_order = temporal_order + ind_order + ";"
        temporal_order = temporal_order[:-1]
        send_msg = code+"]"+target+":"+temporal_order
    elif code == "CARDPLAYED":
        send_msg = code+"]"+target+":"+order
    elif code == "DAMAGE":
        send_msg = code+"]"+str(target)+":"+str(order)
    elif code == "ACARDPLAYED":
        print("card played: "+str(target))
    elif code == "XCARDPLAYED":
        print("move token")
    elif code == "SCARDPLAYED":
        print("move token")
        
    else:
        send_msg = code+"]"+target+":"+order
    
    return send_msg


def main():
    
    code, target, order = recv_msg_translator("BATCH]all:10,3;5,9;6,9")   
    
    print(code)
    print(target)
    print(order) 
    
    code, target, order = recv_msg_translator("VECTORTOGO]all:7,6") 
    print(code)
    print(target)
    print(order) 
    trying = "something"
    trying += " else"
    print(trying)

#main()