#import pygame
import sqlite3
import random
import sys
from dbcreator import alltablesconstructor, individual_list
from dbintermediatefunctions import deckmixer, deck_assigner, drawer, reshuffle_deck, card_counter
from gameobjects import CardObject, TokenObject
from constants import DECKS, FACTIONS, CELL, CARD_WIDTH, FACTION_DECK_POSITION, SPELL_DECK_POSITION, GRID, PRE_GAME_TOKEN_MAT, REQ_FIELDS, ENEMY_FACTION_HAND
#from functionsmodule import movement_blocker
#from pregame_functions import player_token_assigner
from pickleobj import Exchange_object



def conection_sql(database = "currentgame.db"):
    global conector
    conector = sqlite3.connect(database)
    return conector

class Player_Object():
    def __init__(self, player_faction, test = False):
        #self.spells_db = spells_db
        #self.conector = conection_sql(database)
        #self.pointer = self.conector.cursor()
        #self.faction = faction # units_a or units_b
        #self.player_deck = player_deck # cards_a or cards_b
        #self.spell_player_hand = spell_player_hand # player_a or player_b
        
        self.player_faction = player_faction
        
        self.faction_card_fields, self.faction_deck = individual_list("cards.csv", self.player_faction)   # create reference fields and cards lists
        self.player_faction_hand = []
        self.player_hand_objs = []
        self.player_hand = []
        self.player_faction_discard = []
        
        self.spell_card_fields, self.player_spell_deck = individual_list("spells.csv")
        #self.player_spell_deck = []
        self.player_spell_hand_objs = []
        self.player_spell_hand = []
        self.player_spell_discard = []
        
        self.token_list_fields, self.token_list = individual_list("units.csv", self.player_faction)
        self.player_tokens = []
        self.player_dead_tokens = []
        self.to_move_token = None
        
        self.player_exchange_obj = Exchange_object(self.player_faction)
        #if test:
        #    self.token_list_loader()
    def __str__(self) -> str:
        return str(self.player_faction)
    
    def general_list_loader(self):
        
        self.faction_card_fields, self.faction_deck = individual_list("cards.csv", self.player_faction)
        self.spell_card_fields, self.player_spell_deck = individual_list("spells.csv")
        self.token_list_fields, self.token_list = individual_list("units.csv", self.player_faction)
        
        
    def token_list_loader(self): 
        
        #fields, token_list = individual_list("units.csv", self.player_faction)
        pos = 0
        
        for token_inf in self.token_list:
            temp_list = []
            for req in REQ_FIELDS:
                temp_list.append(token_inf[self.token_list_fields.index(req)])
            self.player_tokens.append(TokenObject(CELL, 0, CELL,temp_list[0],temp_list[1],int(temp_list[2]), temp_list[3]))
            pos += 1
    
    def exchanger_method_forward(self):
        
        #player_exchange_object = Exchange_object(self.player_faction)
        self.player_exchange_obj.load_exchange(self.player_faction, self.player_faction_hand, self.player_hand, self.player_faction_discard,self.player_spell_deck, self.player_spell_hand, self.player_spell_discard, self.token_list, self.player_dead_tokens)
        
        return self.player_exchange_obj
    
    def exchanger_method_backward(self):
        
        self.player_faction = self.player_exchange_obj.player_faction
        
        self.player_faction_hand = self.player_exchange_obj.player_faction_hand 
        self.player_hand = self.player_exchange_obj.player_hand 
        self.player_faction_discard = self.player_exchange_obj.player_faction_discard
        
        self.player_spell_deck = self.player_exchange_obj.player_spell_deck
        self.player_spell_hand = self.player_exchange_obj.player_spell_hand
        self.player_spell_discard = self.player_exchange_obj.player_spell_discard
        
        self.token_list = self.player_exchange_obj.token_list
        self.player_dead_tokens = self.player_exchange_obj.player_dead_tokens
                
        
    #### New Method with lists
    def fate_phase(self, xpos = FACTION_DECK_POSITION[0], ypos = FACTION_DECK_POSITION[1], repetitions = 3): #db, deck, player -> ("cards_a", "deck", "hand") //// xpos and ypos are the deck positions
        # FATE PHASE
        # Draw 3 cards from your deck. 
        # Max hand size = 5 cards.
        # If the deck runs out, shuffle the discard and draw from it.
        # Discard excess cards.
        drawn_cards = []
        for i in range(repetitions):
            
            drawn_card_data = self.faction_drawer()
            req_info = ["Card_Name","Type","Range","Notes","Images"]
            drawn_card_info = []
            for inf in req_info:
                drawn_card_info.append(drawn_card_data[(self.faction_card_fields.index(inf))])
            #print("drawn_card_info: ",drawn_card_info)
            self.hand_refresher(drawn_card_info, xpos, ypos, self.player_hand_objs)
            drawn_cards.append(drawn_card_info[0])
        
        return drawn_cards
    
    def enemy_fate_phase(self, order):
        
        name_index = self.faction_card_fields.index("Card_Name")
        for card in self.faction_deck:
            if card[name_index] in order:
                req_info = ["Card_Name","Type","Range","Notes","Images"]
                drawn_card_info = []
                for info in req_info:
                    drawn_card_info.append(card[(self.faction_card_fields.index(info))])
                self.hand_refresher(drawn_card_info, ENEMY_FACTION_HAND.x, ENEMY_FACTION_HAND.y, self.player_hand_objs, ENEMY_FACTION_HAND.height*0.5)
    
    def enemy_card_played(self, target, order):
        
        try:
                
            if target == "faction":
                 
                print("order :",order)
                for card in self.player_hand_objs:
                    if str(card) == order:
                        card_info_name, card_type_info, card_info_image = card.name_show, card.card_type, card.image
                        self.player_hand_objs.remove(card)
                        
            elif target == "spell":
            
                print("order :",order)
                for card in self.player_spell_hand_objs():
                    if str(card) == order:
                        self.player_spell_hand_objs.remove(card)
            
            return card_info_name, card_type_info, card_info_image
                     
        except: print("failed at identifying faction card")
        
           
        
        
        
          
    
    def move_phase(self, codes_tuple):
    
        # MOVE PHASE
        # Play (discard) a Move card to move one of your units.
        # The move card has a number. 
        # This is the number of spaces the unit moves.
        # Moves can be diagonal or orthogonal. 
        # “Knight” type move cards allow a unit to move like a knight in chess.
        # Instead of moving just one unit in any direction, you have the 
        # option of moving one or more units forward the indicated number of 
        # spaces using a single move card.  
        
        if codes_tuple[0] == "M":
            print("movement of range: ", codes_tuple[1])
            
            return codes_tuple[1]
        elif codes_tuple[0] == "XS":
            print("XS card")
            self.xs_card_activation(repetitions= int(codes_tuple[1]))
            return None
        elif codes_tuple[0] == "XF":
            print("XF card")
            self.fate_phase(repetitions = int(codes_tuple[1]))
            return None

       
        
    def attack_phase(self, codes_tuple):
        
        #  """ATTACK PHASE
        #Play (discard) an Attack card to have a unit attack.
        #The attack card has a number. 
        #This is the range of the attack.
        #Attacks can be diagonal or orthogonal. 
        #“Knight” type attack cards produce an attack with a range like a knight in chess.
        #Attacks always do one Hit of damage to the target unless otherwise specified.
        #Use Chits or coins to record damage.
        #A unit reduced to zero Hits is killed and removed from the board.
        #Your opponent may play Defense cards to negate your attack."""     

        
        pass 
    
    def defense_phase(self):
        
        pass   
   
    ### New Method with lists 
    def xs_card_activation(self, xpos = SPELL_DECK_POSITION[0], ypos = SPELL_DECK_POSITION[1], repetitions = 1):
        
        for rep in range(repetitions):
            drawn_card_data = self.spell_drawer()
            req_info = ["Card_Name","Type","Range","Notes","Images"]
            drawn_card_info = []
            for inf in req_info:
                drawn_card_info.append(drawn_card_data[(self.spell_card_fields.index(inf))]) 
        
        self.hand_refresher(drawn_card_info, xpos, ypos, self.player_spell_hand_objs)
    
    
    def faction_drawer(self):
        
        
        if len(self.faction_deck) == 0:
            self.faction_deck = self.player_faction_discard
            self.player_faction_discard = [] 
        
        drawn_card = random.choice(self.faction_deck)
        self.player_faction_hand.append(drawn_card)
        self.faction_deck.remove(drawn_card)

        return drawn_card
    
    def spell_drawer(self):
        
        if len(self.player_spell_deck) == 0:
            self.player_spell_deck = self.player_spell_discard
            self.player_spell_discard = []
        
        drawn_card = random.choice(self.player_spell_deck)
        self.player_spell_hand.append(drawn_card)
        self.player_spell_deck.remove(drawn_card)
        
        return drawn_card
    
    ### New Method for lists
    def hand_refresher(self, drawn_cards, xpos, ypos, card_obj_list, card_size = CARD_WIDTH):  
        
        print("drawn_cards in hand refresher: ",drawn_cards)
        for drawn in drawn_cards:
            print(drawn)
        #drawn_cards = card_data_extractor(self.player_deck, "hand")
        identif_list = []  # list of identifiers of cardobjects
        for crd in card_obj_list:
            identif_list.append(crd.identif)
        try: 
            identif_list.index(drawn_cards[0]) # checks if cardobject already added
        except:
            card_obj_list.append(CardObject(card_size,xpos,ypos,drawn_cards[4],drawn_cards[0],drawn_cards[1],drawn_cards[2])) #adds cardobject
            
        #print(card_obj_list)  
        
    def faction_card_discard(self,card_to_discard_obj):
        
                
        card_index = self.player_hand_objs.index(card_to_discard_obj)
        card_in_list = self.player_faction_hand[card_index]
        self.player_faction_discard.append(card_in_list)
        self.player_faction_hand.remove(card_in_list)
        self.player_hand_objs.remove(card_to_discard_obj)
    
    def spell_card_discard(self, card_to_discard_obj):
        
        identifier = card_to_discard_obj.identif
        for crd in self.player_spell_hand:
            if crd[self.spell_card_fields.index("Card_Name")] == identifier:
                self.player_spell_discard.append(crd)
                self.player_spell_hand.remove(crd)
                self.player_spell_hand_objs.remove(card_to_discard_obj)
                
    def client_test(self):
        return            
                  
    

# Direct Phase Functions        

def new_game_preparations(faction_a, faction_b):    # delete
    
    alltablesconstructor([faction_a, faction_b])
    for deck in DECKS:
        
        deck_assigner(deck)
        deckmixer(deck)
          
def turn_function(db, deck, player):
    
    
    pass


def fate_phase(db, deck, player):
       
    """Draw 3 cards from your deck. 
    Max hand size = 5 cards.
    If the deck runs out, shuffle the discard and draw from it.
    Discard excess cards."""
    
    #pointer = conector.cursor()
    
    for i in range(3):
        sensible = card_counter(db, deck)
        #deckcounter = "SELECT COUNT(*) FROM "+db+" WHERE location='"+deck+"'"
        #print(deckcounter)
        #pointer.execute(deckcounter)
        #deckcount = pointer.fetchone()[0]
        #print("deckcount = ", deckcount, " ", type(deckcount))
        
        if sensible == 0:
            
            reshuffle_deck(db)
            deckmixer(db)
            print("reshufle")
            
        drawer(db,player, deck)    
    #drawer(deck, player)

def move_phase(available_cards):
    
    """MOVE PHASE
    Play (discard) a Move card to move one of your units.
    The move card has a number. 
    This is the number of spaces the unit moves.
    Moves can be diagonal or orthogonal. 
    “Knight” type move cards allow a unit to move like a knight in chess.
    Instead of moving just one unit in any direction, you have the 
    option of moving one or more units forward the indicated number of 
    spaces using a single move card."""  
    
    available_moves = available_cards.copy()
    
    for card in available_cards:
        if card.card_type != "M":
            available_moves.remove(card)
            
    print("available_moves: ",available_moves) 
      
    
def attack_phase():
    """ATTACK PHASE
    Play (discard) an Attack card to have a unit attack.
    The attack card has a number. 
    This is the range of the attack.
    Attacks can be diagonal or orthogonal. 
    “Knight” type attack cards produce an attack with a range like a knight in chess.
    Attacks always do one Hit of damage to the target unless otherwise specified.
    Use Chits or coins to record damage.
    A unit reduced to zero Hits is killed and removed from the board.
    Your opponent may play Defense cards to negate your attack."""     
    
    pass    
        
            
    
def movement(range):
    print("movement: "+range)
  
class Player_Object_test():
    def __init__(self, player_faction, test = False):
        #self.spells_db = spells_db
        #self.conector = conection_sql(database)
        #self.pointer = self.conector.cursor()
        #self.faction = faction # units_a or units_b
        #self.player_deck = player_deck # cards_a or cards_b
        #self.spell_player_hand = spell_player_hand # player_a or player_b
        
        self.player_faction = player_faction
        
        self.faction_card_fields, self.faction_deck = individual_list("cards.csv", self.player_faction)   # create reference fields and cards lists
        self.player_faction_hand = []
        self.player_hand_objs = []
        self.player_hand = []
        self.player_faction_discard = []
        
        self.spell_card_fields, self.player_spell_deck = individual_list("spells.csv")
        #self.player_spell_deck = []
        self.player_spell_hand_objs = []
        self.player_spell_hand = []
        self.player_spell_discard = []
        
        self.token_list_fields, self.token_list = individual_list("units.csv", self.player_faction)
        self.player_tokens = []
        self.player_dead_tokens = []
        self.to_move_token = None
        
        #if test:
        #    self.token_list_loader()    



def main():
    
    pla = Player_Object("INVESTIGATORS")
    pla.general_list_loader()
    pla.token_list_loader()
    print(pla.player_tokens[0])
    
    
def grid_position(position):
    """translates clicks into discrete cell positions

    Args:
        position (tuple): coordinates

    Returns:
        tuple: cell position
    """
    
    x = (position[0]//CELL)#*CELL
    y = (position[1]//CELL)#*CELL
    return (x,y) 

def to_grid(position):
    #pos_in_grid = GRID.index(position)   
    out_of_grid = (position[0]*CELL, position[1]*CELL)
    return out_of_grid
    
if __name__ == "__main__":
    
    #main()
    pass