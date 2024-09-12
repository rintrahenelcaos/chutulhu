import pygame
import sqlite3
import random
from dbcreator import alltablesconstructor, individual_list
from dbintermediatefunctions import deckmixer, deck_assigner, drawer, reshuffle_deck, card_counter, card_data_extractor, token_extractor
from gameobjects import CardObject, TokenObject
from constants import DECKS, FACTIONS, CELL, CARD_WIDTH, FACTION_DECK_POSITION, SPELL_DECK_POSITION, GRID, PRE_GAME_TOKEN_MAT
from functionsmodule import movement_blocker
#from pregame_functions import player_token_assigner



def conection_sql(database = "currentgame.db"):
    global conector
    conector = sqlite3.connect(database)
    return conector

class Player_Object():
    def __init__(self, database, faction ,player_deck, spell_player_hand, player_faction):
        #self.spells_db = spells_db
        self.conector = conection_sql(database)
        self.pointer = self.conector.cursor()
        self.faction = faction # units_a or units_b
        self.player_deck = player_deck # cards_a or cards_b
        self.spell_player_hand = spell_player_hand # player_a or player_b
        
        self.faction_card_fields, self.faction_deck = individual_list("cards.csv", player_faction)   # create reference fields and cards lists
        self.player_faction_hand = []
        self.player_hand_objs = []
        self.player_hand = []
        self.player_faction_discard = []
        
        self.spell_card_fields, self.player_spell_deck = individual_list("spells.csv")
        #self.player_spell_deck = []
        self.player_spell_hand_objs = []
        self.player_spell_hand = []
        self.player_spell_discard = []
        
        self.player_tokens = []
        self.to_move_token = None
        
    def token_list_loader(self): pass    
        
    def fate_phase(self, xpos = FACTION_DECK_POSITION[0], ypos = FACTION_DECK_POSITION[1], repetitions = 3): #db, deck, player -> ("cards_a", "deck", "hand") //// xpos and ypos are the deck positions
        
        # FATE PHASE
        # Draw 3 cards from your deck. 
        # Max hand size = 5 cards.
        # If the deck runs out, shuffle the discard and draw from it.
        # Discard excess cards.
        for i in range(repetitions):
            
            
            sensible = card_counter(self.player_deck, "deck")
            
            if sensible == 0:

                reshuffle_deck(self.player_deck)
                deckmixer(self.player_deck)
                print("reshufle")

            drawer(self.player_deck, "hand", "deck")
            self.hand_refresher(card_data_extractor(self.player_deck, "hand"), xpos, ypos, self.player_hand_objs)  
    
    #### New Method with lists
    def fate_phase(self, xpos = FACTION_DECK_POSITION[0], ypos = FACTION_DECK_POSITION[1], repetitions = 3): #db, deck, player -> ("cards_a", "deck", "hand") //// xpos and ypos are the deck positions
        # FATE PHASE
        # Draw 3 cards from your deck. 
        # Max hand size = 5 cards.
        # If the deck runs out, shuffle the discard and draw from it.
        # Discard excess cards.
        for i in range(repetitions):
            
            drawn_card_data = self.faction_drawer()
            req_info = ["Card_Name","Type","Range","Notes","Images"]
            drawn_card_info = []
            for inf in req_info:
                drawn_card_info.append(drawn_card_data[(self.faction_card_fields.index(inf))])
        print(drawn_card_info)
        self.hand_refresher(drawn_card_info, xpos, ypos, self.player_hand_objs)
        
        
    
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

        #available_moves = self.player_hand.copy()
#
        #for card in self.player_hand:
        #    if card.card_type != "M":
        #        available_moves.remove(card)
#
        #print("available_moves: ",available_moves)
        
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
    
    def hand_refresher(self, drawn_cards, xpos, ypos, card_obj_list):  
        
        #drawn_cards = card_data_extractor(self.player_deck, "hand")
        for drawn in drawn_cards:
            identif_list = []   # list of identifiers of cardobjects
            for crd in card_obj_list:
                identif_list.append(crd.identif)
            try: 
                identif_list.index(drawn[0]) # checks if cardobject already added
            except:
                card_obj_list.append(CardObject(CARD_WIDTH,xpos,ypos,drawn[4],drawn[0],drawn[1],drawn[2])) #adds cardobject
            #hand_card_list = list(set(hand_card_list))
    
    def xs_card_activation(self, xpos = SPELL_DECK_POSITION[0], ypos = SPELL_DECK_POSITION[1], repetitions = 1):
        
        for rep in range(repetitions):
            sensible = card_counter("spells", "deck") 
            if sensible == 0:

                reshuffle_deck("spells")
                deckmixer("spells")
                print("reshufle spells")

            drawer("spells", self.spell_player_hand, "deck")
            self.hand_refresher(card_data_extractor("spells", self.spell_player_hand), xpos, ypos, self.player_spell_hand_objs)
    
    ### New Method with lists 
    def xs_card_activation(self, xpos = SPELL_DECK_POSITION[0], ypos = SPELL_DECK_POSITION[1], repetitions = 1):
        
        for rep in range(repetitions):
            drawn_card_data = self.spell_drawer()
            req_info = ["Card_Name","Type","Range","Notes","Images"]
            drawn_card_info = []
            for inf in req_info:
                drawn_card_info.append(drawn_card_data[(self.spell_card_fields.index(inf))]) 
        
        self.hand_refresher(drawn_card_info, xpos, ypos, self.player_spell_hand_objs)
        
        
            
    def player_token_assigner(self):
        
        #token_mat_positions = [(x,y)for x in range(8) for y in range(2)]
        list_of_tokens = token_extractor(self.faction)
        pos = 0
        for token_inf in list_of_tokens:
            self.player_tokens.append(TokenObject(CELL, 0, CELL,token_inf[0],token_inf[1],int(token_inf[2]), token_inf[3]))
            pos += 1
    
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
            
        
        
    """def player_deck_creator(self):
        
        fields, rows = individual_list("cards.csv")
        for row in rows:
            self.faction_deck.append(CardObject(CELL, 0,0,))"""
        
            



# Direct Phase Functions        

def new_game_preparations(faction_a, faction_b):
    
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
  
    

def main():
    
    new_game_preparations()
    conector = conection_sql()
    #print(deckmixer("spells"))
    #deck_assigner("spells")
    pointer = conector.cursor()
    changer = "UPDATE spells SET location='discard'"
    pointer.execute(changer)
    conector.commit()
    reshuffle_deck("spells")
    deckmixer("spells")
    
    idcount = "SELECT MAX(id) FROM spells"
    pointer.execute(idcount)
    cardcount = pointer.fetchall()[0][0]
    print(cardcount)
    
    for i in range(cardcount):
        print(i)
        #drawer("spells", "discard")
        fate_phase("spells", 'deck',"discard")
        #drawer("spells", "discard", "deck")
        print(i)
        
        
    
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #drawer("spells")
    #reshuffle_deck("spells")

def main():
    
    pass
    
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
    
    main()
    