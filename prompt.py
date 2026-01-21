# prompt.py
def build_prompt(grid, player):
    return f"""
Morpion 10x10. Objectif: aligner 5.
0=vide, 1=X, 2=O.

Joueur actuel: {player}
Grille:
{grid}

Réponds avec un seul coup. Format idéal: Coup: r,c
(mais tu peux aussi répondre: r,c)
"""
