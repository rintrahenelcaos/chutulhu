import pickle

class Player():
    
    def __init__(self, textual) -> None:
        self.textual = textual
    def test(self):
        return self.textual
    def __str__(self) -> str:
        return str(self.textual)
    
pick = [Player("player 1"), Player("player 2")]

print(pick)
    
print(pick[0])

serialized_data = pickle.dumps(pick)

print(serialized_data)

deserialized_data = pickle.loads(serialized_data)

print(deserialized_data)
deserialized_data[0].textual = "Player 1"
print(deserialized_data[0])