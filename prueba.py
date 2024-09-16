import pickle
from dbcreator import individual_list
from constants import REQ_FIELDS, CELL
from gameobjects import TokenObject 
class Player():
    
    def __init__(self, textual) -> None:
        self.textual = textual
        self.player_tokens = []
        self.player_faction = "DEEP_ONES"
    def test(self):
        return self.textual
    def __str__(self) -> str:
        return str(self.textual)
    
    def token_list_loader(self): 
        
        fields, token_list = individual_list("units.csv", self.player_faction)
        pos = 0
        
        for token_inf in token_list:
            temp_list = []
            for req in REQ_FIELDS:
                temp_list.append(token_inf[fields.index(req)])
            self.player_tokens.append(TokenObject(CELL, 0, CELL,temp_list[0],temp_list[1],int(temp_list[2]), temp_list[3]))
            pos += 1
    
pick = [Player("player 1"), Player("player 2")]
"""
print(pick)
    
print(pick[0])

serialized_data = pickle.dumps(pick)

print(serialized_data)

deserialized_data = pickle.loads(serialized_data)

print(deserialized_data)
deserialized_data[0].textual = "Player 1"
print(deserialized_data[0])"""

pl = Player("player 1")
pl.token_list_loader()
print(pl.player_tokens)
for token in pl.player_tokens:
    print(token)