def build_prompt(grid, player):
    return f"""
Morpion 10x10. Objectif: aligner 5.
0=vide, 1=X, 2=O.

Joueur actuel: {player}
Grille:
{grid}

Règles strictes :
1. ANALYSE : Vérifie chaque ligne, colonne et DIAGONALE pour un alignement de 4.
2. Si vous pouvez aligner 5 maintenant, faites-le immédiatement. C'est la priorité absolue.
3. Sinon, bloquez si l'adversaire peut aligner 5 au prochain tour (si l'adversaire a 4 pions alignés).
4. Sinon, choisissez le meilleur coup stratégique pour progresser vers 5.
5. Réponds avec un seul coup sous la forme: r,c (ligne,colonne)
6. Ne joue qu’à ton tour. Si ce n’est pas ton tour, ne fais rien.

Note : Les lignes commencent à 0 en haut et les colonnes à 0 à gauche.
Ne fais jamais plus d'un coup à la fois.
Réponds avec un seul coup. Format idéal: Coup: r,c
"""