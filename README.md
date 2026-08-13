# Projet 2 : Explorer et comprendre les performances des employés (Python ou R)

## Problématique
Une entreprise souhaite analyser la répartition des performances des employés pour comprendre les écarts et identifier les outliers.

## Objectif
Étudier les distributions des scores de performance et des heures travaillées pour détecter les facteurs d’amélioration.

## Compétences à acquérir
Statistiques descriptives : Moyenne, médiane, mode, quartiles, variance, écart-type. Visualisation : histogrammes, boxplots, pie chart, diagramme en barre. Détection des outliers avec la règle 1.5×IQR. Manipulation des données avec pandas ou dplyr.

## Base de données recommandée
HR Analytics Dataset

## Démarrage
1. Récupérer ou générer le dataset recommandé.
2. Ouvrir l’outil adapté : Excel pour le projet 1, SQL pour le projet 5/8, Python/R pour les autres.
3. Créer une analyse claire, des visualisations et un livrable final.


## Stack Technique Utilisée

### Langages & Environnement
- **Python 3.x** : langage de programmation principal pour la data science
- **Venv (Virtual Environment)** : environnement isolé pour gérer les dépendances Python sans conflits système

### Bibliothèques Python

| Bibliothèque | Version | Rôle |
|---|---|---|
| **NumPy** | - | Calculs numériques, génération de nombres aléatoires, opérations mathématiques |
| **Pandas** | - | Manipulation de données (DataFrames), nettoyage, agrégations, export CSV |
| **Matplotlib** | - | Création de graphiques statiques (courbes, histogrammes, graphiques personnalisés) |
| **Seaborn** | - | Visualisation statistique avancée (boxplots, heatmaps, distributions) |

### Outils & Format
- **CSV** : format de stockage des données (texte simple, universel, facilement importable)
- **PNG** : format d'export des graphiques (images compressées, haute qualité)

---

## Comment ça marche : Guide Complet

### 1. Préparation de l'Environnement

#### Qu'est-ce qu'un Virtual Environment (venv) ?
Un venv est une **bulle isolée** où tu installes des bibliothèques Python spécifiques à ton projet, sans affecter le Python système. Avantages :
- ✅ Pas de conflits de versions entre projets
- ✅ Tu peux avoir plusieurs projets avec différentes versions de pandas/numpy
- ✅ Facile à "détruire" et recommencer si besoin

#### Commandes pour le créer et l'utiliser
```bash
# Créer le venv
python3 -m venv .venv

# Activer le venv (sur Linux/Mac)
source .venv/bin/activate

# Sur Windows, c'est :
# .venv\Scripts\activate

# Tu vois maintenant "(.venv)" au début de ta ligne terminal
# Pour désactiver plus tard :
deactivate
```

#### Installation des dépendances
```bash
# Voir/créer le fichier requirements.txt (liste les bibliothèques)
cat requirements.txt

# Installer toutes les bibliothèques listées
pip install -r requirements.txt
```

---

### 2. Le Script Python : Étape par Étape

#### **Étape 1 : Imports** (les outils qu'on va utiliser)
```python
import numpy as np          # Pour les maths et nombres aléatoires
import pandas as pd         # Pour les tableaux de données
import matplotlib.pyplot as plt  # Pour les graphiques
import seaborn as sns       # Pour les graphiques statistiques
```

#### **Étape 2 : Générer un Dataset de Démonstration**
Comme tu n'as pas accès à Kaggle ici, le script **simule** un dataset HR réaliste :

```python
np.random.seed(42)  # Graine pour reproductibilité (mêmes chiffres à chaque exécution)
n_employees = 200   # 200 employés simulés

# Créer des données réalistes avec des distributions normales
performance_score = np.random.normal(loc=70, scale=12, size=n_employees)
# = scores centrés autour de 70, avec une variation de 12 points
# np.clip(min=30, max=100) = limiter entre 30 et 100 (score réaliste)

hours_worked = np.random.normal(loc=42, scale=5, size=n_employees)
# = environ 42h/semaine (norme), avec variation de 5h
```

**Concepts clés** :
- **Distribution normale** : la plupart des valeurs sont proches de la moyenne (70), quelques outliers loin
- **np.clip()** : force les valeurs à rester dans une plage réaliste [min, max]
- **np.random.seed(42)** : assure que tes tests restent reproductibles

#### **Étape 3 : Ajouter des Outliers Intentionnels**
```python
performance_score[[5, 27, 73]] = [20, 95, 99]
# Employees 5, 27, 73 ont des scores extrêmes
# = des cas à identifier comme anormaux
```

#### **Étape 4 : Créer un DataFrame Pandas**
```python
employee_data = pd.DataFrame({
    "EmployeeID": range(1, n_employees + 1),
    "Department": ["Sales", "Marketing", ...],  # Catégories d'employés
    "PerformanceScore": performance_score,      # Variable continue
    "HoursWorked": hours_worked,                # Variable continue
    "Age": np.random.randint(22, 60, ...),     # Variable discrète (entiers)
})
```

**Ce que c'est** : un tableau Excel en Python avec lignes = employés, colonnes = variables.

#### **Étape 5 : Statistiques Descriptives**
```python
employee_data.describe()  # Voir : mean, std, min, Q1, median, Q3, max
employee_data.groupby("Department")["PerformanceScore"].mean()
# = score moyen par département
```

**Concepts** :
- **Moyenne (mean)** : la somme ÷ nombre (valeur centrale)
- **Médiane (median)** : la valeur du milieu (moins affectée par outliers)
- **Écart-type (std)** : mesure la dispersion autour de la moyenne
- **Quartiles** : découpe les données en 4 parties égales (Q1=25%, Q3=75%)

#### **Étape 6 : Visualisations Statiques**
```python
# Histogramme avec courbe de densité
sns.histplot(employee_data['PerformanceScore'], kde=True, bins=20)
plt.savefig('distribution_performance.png')

# Boxplot par département
sns.boxplot(x='Department', y='PerformanceScore', data=employee_data)
plt.savefig('performance_by_department.png')
```

**À quoi ça sert** :
- **Histogramme** : voir la forme de la distribution (symétrique ? bimodale ?)
- **Boxplot** : détecter outliers visuellement + comparer groupes
- **KDE (Kernel Density Estimate)** : courbe lisse de la distribution

#### **Étape 7 : Détection des Outliers (Règle IQR)**
```python
Q1 = data.quantile(0.25)  # 25e percentile
Q3 = data.quantile(0.75)  # 75e percentile
IQR = Q3 - Q1             # Interquartile Range

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data < lower_bound) | (data > upper_bound)]
```

**Explication** : tout ce qui est en dehors de [Q1 - 1.5×IQR, Q3 + 1.5×IQR] est suspect.

---

### 3. Les Datasets : Où les Trouver & Ce Qu'ils Signifient

#### **HR Analytics Dataset** (celui qu'on utilise ici)
- **Lien réel** : [Kaggle - HR Analytics Job Change](https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists)
- **Colonnes** : EmployeeID, Department, Performance Score, Hours Worked, Age, Satisfaction, ...
- **Signification** : données RH d'une entreprise pour analyser performances, turnover, satisfaction
- **Ici, on l'a simulé** : parce que pas d'accès direct à Kaggle, on a généré des données réalistes

#### **Superstore Dataset** (pour les projets 1 & 3)
- **Lien** : [Kaggle - Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **Colonnes** : Order ID, Sales, Profit, Region, Category, Sub-Category, ...
- **Signification** : données de ventes d'une chaîne logistique (Excel + Power BI)

#### **Chinook Database** (pour le projet 5 - SQL)
- **Lien** : [GitHub - Chinook Database](https://github.com/lerocha/chinook-database)
- **Colonnes** : Customers, Orders, Invoices, Tracks, Artists, ...
- **Signification** : base de données musicale (magasin digital de musique)

#### **Wine Quality Dataset** (pour le projet 6 - ACP)
- **Lien** : [UCI ML Repository - Wine Quality](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- **Colonnes** : alcohol, acidity, sulfates, quality score, ...
- **Signification** : propriétés chimiques des vins + note de qualité

---

## Fichiers Générés par le Script

### Fichiers Créés (au premier lancement)
- `hr_analytics_demo.csv` : le dataset simulé en format CSV
- `distribution_performance.png` : histogramme des scores de performance
- `distribution_hours.png` : histogramme des heures travaillées
- `performance_by_department.png` : boxplot performances par département
- `hours_by_department.png` : boxplot heures par département
- `correlation_matrix.png` : heatmap des corrélations entre variables

### Ces fichiers sont importants pour
- **Analyser** : comprendre les patterns dans les données
- **Documenter** : montrer tes résultats dans un rapport
- **Déboguer** : vérifier que tes données ne sont pas bizarres

---

## Comment Lancer le Script

### Option A : Avec le venv activé (Recommandée)
```bash
cd /home/kashira/knowledge/dev_ia/HR_performance
source .venv/bin/activate
python projet2_analyse_employes.py
```

### Option B : Sans activation (chemin complet)
```bash
./.venv/bin/python3 projet2_analyse_employes.py
```

### Option C : Depuis un sous-dossier
```bash
cd Projet_2_Explorer_et_comprendre_les_performances_des_employés_Python_ou_R
../../.venv/bin/python3 projet2_analyse_employes.py
```

---

## Concepts Clés à Retenir

| Concept | Définition | Utilisé Pour |
|---|---|---|
| **Venv** | Environnement Python isolé | Éviter conflits de dépendances |
| **Pandas DataFrame** | Tableau de données en Python | Manipuler des fichiers CSV/Excel |
| **Numpy Array** | Tableau de nombres pour maths | Calculs, statistiques, simulations |
| **Matplotib/Seaborn** | Créer des graphiques | Visualiser distributions, tendances |
| **Distribution Normale** | Courbe en cloche (Gauss) | Modéliser données réalistes |
| **Outliers (Anomalies)** | Valeurs très loin de la moyenne | Identifier cas exceptionnels |
| **IQR (Interquartile Range)** | Q3 - Q1 | Détecter outliers statistiquement |
| **Corrélation** | Lien entre deux variables | Voir si X influence Y |

---

## Fichiers déjà présents
- `projet2_analyse_employes.py` : script Python de démonstration pour générer et analyser un dataset HR Analytics.
- `requirements.txt` : liste des dépendances Python à installer

