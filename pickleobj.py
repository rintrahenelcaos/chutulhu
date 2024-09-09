import pickle

class Exchange_object():
    

    def __init__(self, something) -> None:
        self.something = something
        
    def __str__(self) -> str:
        return str(self.something)