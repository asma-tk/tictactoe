def build_prompt(grid, player):
    rows = "\n".join(" ".join(map(str, row)) for row in grid)

    return f"""
Tu joues au Morpion 10x10.
Objectif: aligner 5 symboles.

0 = vide, 1 = X, 2 = O
Tu es le joueur {player}.

RÈGLES IMPORTANTES:
- Si tu peux gagner en un coup, fais-le.
- Sinon, bloque immédiatement un alignement adverse de 4.
- Sinon, joue près de tes propres symboles.
- Ne joue jamais au hasard.
- r et c sont entre 0 et 9 (indices 0-based).

Grille actuelle:
{rows}

Réponds uniquement par:
Coup: r,c
"""
