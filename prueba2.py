from game_network import Network

net = Network()
net.connect("hello")

run = True
while run:
    decide = input("decide: ")
    if decide == "send":
        
        sending = input("mensaje: ")
        try:
            net.send_only(sending)
        except:
            print("failed sending")
            
    elif decide == "listen":
        
        try: 
            recieved = net.recieve_only() 
            print("recieved: ",recieved)
        except: 
            print("failed listening")
            
    
        
        
        
        