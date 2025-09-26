import enemy_defense
import enemy_strength


enemy_defense.process_defense()
print()
for x in range(1, 4):
    enemy_strength.process_strength(x, False)
    enemy_strength.process_strength(x, True)
