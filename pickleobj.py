import pickle

class Exchange_object:
    

    def __init__(self, identifier) -> None:
        
        self.identifier = identifier
        
        self.player_faction = str
        
        self.player_faction_hand = []
        self.player_hand = []
        self.player_faction_discard = []
        
        self.player_spell_deck = []
        self.player_spell_hand = []
        self.player_spell_discard = []
        
        self.token_list = []
        self.player_dead_tokens = []
        
        
    def __str__(self) -> str:
        return str(self.identifier)
    
    def load_exchange(self, player_faction_hand, player_hand, player_faction_discard, player_spell_deck, player_spell_hand, player_spell_discard, token_list, player_dead_tokens):
        
        self.player_faction_hand = player_faction_hand
        self.player_hand = player_hand
        self.player_faction_discard = player_faction_discard
        
        self.player_spell_deck = player_spell_deck
        self.player_spell_hand = player_spell_hand
        self.player_spell_discard = player_spell_discard
        
        self.token_list = token_list
        self.player_dead_tokens = player_dead_tokens
    
    def unload_exchange(self):
        pass
        return         
