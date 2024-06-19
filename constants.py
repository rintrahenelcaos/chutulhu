DECKS = ["spells", "cards_a", "cards_b"]


FACTIONS = ["INVESTIGATORS","DEEP_ONES", "CULTIST","SERPENT_PEOPLE"]

ROWS = 8
COLUMNS = 8
#CELL = 100

BACKGROUND_COLOR = (0,0,0)

GRID = [(x, y) for x in range(8) for y in range(8)]
GRID_DIC = {}
for cell in GRID:
    GRID_DIC.update({cell:"None"})

FPS = 60