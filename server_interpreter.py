
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
            print("cards drawn")
        elif code == "MCARDPLAYED":
            print("card played")
        elif code == "ACARDPLAYED":
            print("move token")
        elif code == "XCARDPLAYED":
            print("move token")
        elif code == "SCARDPLAYED":
            print("move token")



        return code, target, order
    
    
    

def send_msg_translator(code, target, order):
    
    
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