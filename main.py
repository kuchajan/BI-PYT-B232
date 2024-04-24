# Game state: Main menu, Play menu, Playing level, Level editor menu, Editing level

# Main meWindow nu: Play, Level editor, Exit
# Play menu: Choose level, Back
# Level editor menu: Choose level, Create new, Back

from Level import Level

level = Level("levels/level1.lvl")
print(level.optimalMoves)
