# prompt.py
def build_prompt(grid, player):
    return f"""
Morpion 10x10. Objectif: aligner 5.
0=vide, 1=X, 2=O.

Joueur actuel: {player}
Grille:
{grid}

Règles strictes :
1. Si vous pouvez aligner 5 maintenant, faites-le immédiatement.
2. Sinon, bloquez si l'adversaire peut aligner 5 au prochain tour.
3. Sinon, choisissez le meilleur coup stratégique pour progresser vers 5.
4. Réponds avec un seul coup sous la forme: r,c (ligne,colonne)
5. Ne joue qu’à ton tour. Si ce n’est pas ton tour, ne fais rien.

Ne fais jamais plus d'un coup à la fois.
Réponds avec un seul coup. Format idéal: Coup: r,c
(mais tu peux aussi répondre: r,c)

"""
