# mini-pipeline-Dymola


## Objectif

Mini-pipeline Python pour :

- Charger un fichier `.mat` Dymola
- Extraire les séries temporelles et les variables statiques / géométriques
- Identifier automatiquement les signaux dynamiques
- Générer des courbes pour les signaux clés
- Exporter les séries temporelles en CSV
- Exporter les variables statiques en JSON

Cette approche permet d’analyser rapidement n’importe quel fichier Dymola sans connaître à l’avance le nom des variables.

---

## Architecture

.mat Dymola
├─ Timeseries → CSV
├─ Static / Parameters / Geometry → JSON
└─ Plots → Graphiques matplotlib

**Pipeline :**

1. Chargement du fichier `.mat` via DyMat
2. Extraction des séries temporelles et variables statiques
3. Détection automatique des signaux clés :
   - Toutes les colonnes qui **varient réellement dans le temps** (`nunique() > 1`)
4. Génération de plots pour les signaux clés
5. Export CSV pour les séries temporelles
6. Export JSON pour les données statiques

---

## Structure du dépôt

dyma_pipeline/
├── data/raw/ # fichiers .mat
├── outputs/
│ ├── csv/ # fichiers CSV des séries temporelles
│ ├── json/ # fichiers JSON des variables statiques
│ └── plots/ # graphiques matplotlib des signaux dynamiques
└── dyma_reader.py # script principal

---

## Utilisation

```bash
python dyma_reader.py data/raw/Fichier.mat
Génère CSV : outputs/csv/Fichier.csv

Génère JSON : outputs/json/Fichier_static.json

Génère plots : outputs/plots/*.png

Notes techniques
Les séries temporelles sont détectées automatiquement comme les colonnes qui varient dans le temps.

Les variables constantes, géométriques ou paramètres sont exportées dans un fichier JSON.

Optimisé pour fichiers Dymola volumineux.

Compatible avec tous les fichiers .mat standards de Dymola.
```
