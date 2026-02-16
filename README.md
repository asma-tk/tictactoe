LLM vs LLM — Tic Tac Toe (10x10 / 5-in-a-row) 

Description Ce projet est une simulation d’un Tic Tac Toe sur une grille
10x10 avec une condition de victoire de 5 pions alignés (horizontale,
verticale, diagonales).

Le but est de fournir une logique de jeu simple (moteur) qui peut être
utilisée pour : - faire jouer deux IA / deux agents (ex: LLM vs LLM) -
tester des stratégies - brancher une interface (CLI / Web) plus tard

Règles du jeu - Deux joueurs : X et O - Grille : 10 x 10 - Tour par tour
: chaque joueur place un pion dans une case vide - Victoire : 5 pions
alignés - Match nul : grille pleine sans gagnant

Fichiers - game.py : moteur du jeu (grille, coups, victoire, match nul)

Fonctionnement du moteur (Game)

Constantes : EMPTY = 0, X = 1, O = 2 WIN_LEN = 5 : longueur d’alignement
gagnante

Méthodes principales : - reset() : réinitialise la grille et remet le
joueur courant à X - valid(r, c) : vérifie qu’un coup est dans la grille
et sur une case vide - play(r, c) : joue un coup si valide, puis change
de joueur - winner() : détecte un gagnant (X ou O) dans 4 directions -
draw() : match nul si la grille est pleine et aucun gagnant -
fallback_move() : stratégie simple pour choisir une case proche du
centre

Exemple d’utilisation

from game import Game, X, O

g = Game(size=10) g.play(5, 5) # X g.play(5, 6) # O

w = g.winner() if w == X: print(“X gagne”) elif w == O: print(“O gagne”)
elif g.draw(): print(“Match nul”) else: print(“Partie en cours”)

Ce que j’ai appris - Représenter une grille et un état de jeu en
Python - Vérifier la validité des actions - Détecter une condition de
victoire dans plusieurs directions - Construire une stratégie simple

Améliorations possibles - Ajouter un mode LLM vs LLM (agents
automatiques) - Ajouter un mode human vs bot - Ajouter une interface
utilisateur - Ajouter des logs ou replays

Auteur Ahmad Abo-Alola
