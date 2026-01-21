# prompt.py
def build_prompt(grid, player):
    return f"""
Tu joues au Morpion 10x10. Victoire: aligner 5 symboles.
Valeurs: 0=vide, 1=X, 2=O.

Joueur actuel: {player}
Grille:
{grid}

IMPORTANT:
Tu dois répondre .
Aucun texte . Aucune phrase.
Format EXACT:
Coup: r,c
"""

