# 🕹️ LLM vs LLM — Morpion 10×10

Un jeu de Morpion sur une grille **10×10** où deux **LLMs** s'affrontent coup par coup. L'interface est construite avec **Streamlit**, le backend avec **FastAPI**, et les modèles sont hébergés sur **Azure OpenAI**.

---

## 🎯 Règles du jeu

| Paramètre | Valeur |
|-----------|--------|
| Grille | 10 × 10 |
| Joueurs | X (Bleu) vs O (Rouge) |
| Condition de victoire | 5 pions alignés (horizontal, vertical, diagonal) |
| Match nul | Grille pleine sans gagnant |

---

## 🗂️ Structure du projet

```
tictactoe/
├── api.py             # Backend FastAPI (endpoints, appel Azure, parsing du coup)
├── app_streamlit.py   # Interface utilisateur Streamlit
├── game.py            # Moteur du jeu (grille, coups, victoire, match nul)
├── models_config.py   # Configuration des modèles Azure disponibles
├── prompt.py          # Construction du prompt envoyé au LLM
├── style.css          # Styles CSS pour le plateau de jeu
├── requirements.txt   # Dépendances Python
└── Procfile           # Démarrage des services (API + Streamlit)
```

---

## 🤖 Modèles disponibles

| Label | Déploiement Azure |
|-------|------------------|
| GPT-4o | `morpion-openai` |
| gpt-4.1-mini | `morpion-mini` |

---

## ⚙️ Installation

```bash
# Cloner le repo
git clone https://github.com/asma-tk/tictactoe.git
cd tictactoe

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Variables d'environnement requises

```bash
export AZURE_OPENAI_ENDPOINT="https://<votre-ressource>.openai.azure.com"
export AZURE_OPENAI_KEY="<votre-clé>"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"  # optionnel
```

---

## 🚀 Lancement

```bash
# Terminal 1 — API FastAPI
uvicorn api:app --reload --port 8000

# Terminal 2 — Interface Streamlit
streamlit run app_streamlit.py
```

Ou via le `Procfile` si vous utilisez un gestionnaire de processus (ex: `honcho`).

---

## 🧠 Fonctionnement du moteur (`game.py`)

| Méthode | Description |
|---------|-------------|
| `reset()` | Réinitialise la grille et remet le joueur courant à X |
| `valid(r, c)` | Vérifie qu'un coup est dans la grille et sur une case vide |
| `play(r, c)` | Joue un coup si valide, puis change de joueur |
| `winner()` | Détecte un gagnant dans 4 directions |
| `draw()` | Match nul si grille pleine et aucun gagnant |
| `fallback_move()` | Stratégie de repli : case vide proche du centre |

---

## 🖥️ Interface Streamlit

- **Relancer Jeu** : réinitialise la partie
- **Jouer Coup IA** : fait jouer le LLM du joueur courant
- **Auto** : mode automatique — les deux LLMs jouent en continu
- **Vitesse** : délai entre chaque coup en mode auto (0.05s → 1s)
- Sélection indépendante du modèle pour **X** et **O**

---

## 👤 Auteur

**Asma Taberko**
