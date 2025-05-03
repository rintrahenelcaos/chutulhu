import random

numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]

def ticket_creator(number, numbers):
    
    listed = numbers.copy()
    random.shuffle(listed)
    listed.remove(number)
    
    tickets = []
    
    for i in range(len(listed)):
        tick = []
        tick.append(number)
        pos = i
        tick.append(listed[pos])
        
        if pos == len(listed)-1:
            
            tick.append(listed[0])
            tick.append(listed[1])
            tick.append(listed[2])
        elif pos ==len(listed)-2:
            tick.append(listed[pos+1])
            tick.append(listed[0])
            tick.append(listed[1])
        elif pos ==len(listed)-3:
            tick.append(listed[pos+1])
            tick.append(listed[pos+2])
            tick.append(listed[0])
        else:
            tick.append(listed[pos+1])
            tick.append(listed[pos+2])
            tick.append(listed[pos+3])
        
        tickets.append(tick)
    return tickets
        
def lottery(tickets, numbers):
    
    lotto5 = random.sample(numbers, 5)
    print(lotto5)
    
    for tick in tickets:
        matches = list(set(tick).intersection(lotto5))
        print(len(matches))
    
tickets_out = ticket_creator(5,numbers)
print((tickets_out))
lottery(tickets_out, numbers)