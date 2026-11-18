"""
Projet 2 : Explorer et comprendre les performances des employés
Python / pandas / seaborn

Objectif : étudier les distributions des scores de performance et des heures travaillées,
identifier des outliers et visualiser les tendances.

Ce script génère un dataset de démonstration si aucun jeu de données n'est fourni.
Avec --data, il analyse votre propre export RH en CSV.

Il termine par un score de contribution (0-100) qui classe les employés selon
leur performance, leur efficacité (performance par heure travaillée) et leur
satisfaction, puis affiche le top N.

Usage :
    python projet2_analyse_employes.py                      # dataset de démonstration
    python projet2_analyse_employes.py --data mes_rh.csv    # vos données
    python projet2_analyse_employes.py --data mes_rh.csv --top 5
"""

import argparse
import sys

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

# Colonnes nécessaires à l'analyse et au score
REQUIRED_COLUMNS = ["EmployeeID", "Department", "PerformanceScore", "HoursWorked", "Satisfaction"]

# Poids du score de contribution (somme = 1). La performance pèse le plus ;
# l'efficacité récompense qui produit beaucoup sans heures excessives ;
# la satisfaction reflète l'engagement, qui compte pour le collectif.
SCORE_WEIGHTS = {"Performance": 0.5, "Efficacite": 0.3, "Satisfaction": 0.2}

parser = argparse.ArgumentParser(description="Analyse des performances des employés et classement par contribution.")
parser.add_argument("--data", help="chemin d'un export RH en CSV (sinon : dataset de démonstration)")
parser.add_argument("--top", type=int, default=10, help="nombre d'employés à afficher dans le classement (défaut : 10)")
args = parser.parse_args()
if args.top < 1:
    parser.error("--top doit être au moins 1")


def load_employee_data(path):
    """Charge un CSV RH, vérifie les colonnes et écarte les lignes inutilisables."""
    try:
        data = pd.read_csv(path)
    except FileNotFoundError:
        sys.exit(f"Fichier introuvable : {path}")
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        sys.exit(f"Colonnes manquantes dans {path} : {', '.join(missing)}\nColonnes attendues : {', '.join(REQUIRED_COLUMNS)}")
    for col in ["PerformanceScore", "HoursWorked", "Satisfaction"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    before = len(data)
    data = data.dropna(subset=REQUIRED_COLUMNS)
    data = data[data["HoursWorked"] > 0]
    if len(data) < before:
        print(f"{before - len(data)} ligne(s) écartée(s) : valeurs manquantes, non numériques ou heures nulles.")
    if data.empty:
        sys.exit("Aucune ligne exploitable dans le fichier.")
    return data.reset_index(drop=True)


def generate_demo_data():
    """Jeu de données de démonstration : 200 employés simulés, avec quelques outliers."""
    np.random.seed(42)

    n_employees = 200

    departments = ["Sales", "Marketing", "Finance", "HR", "Operations", "IT"]
    segments = ["Junior", "Mid", "Senior"]

    # Simuler des scores de performance et des heures travaillées
    performance_score = np.clip(np.random.normal(loc=70, scale=12, size=n_employees), 30, 100)
    hours_worked = np.clip(np.random.normal(loc=42, scale=5, size=n_employees), 30, 60)

    # Ajouter quelques outliers
    performance_score[[5, 27, 73]] = [20, 95, 99]
    hours_worked[[12, 56, 145]] = [25, 65, 70]

    employee_data = pd.DataFrame({
        "EmployeeID": range(1, n_employees + 1),
        "Department": np.random.choice(departments, size=n_employees, p=[0.22, 0.18, 0.16, 0.14, 0.18, 0.12]),
        "Segment": np.random.choice(segments, size=n_employees, p=[0.4, 0.4, 0.2]),
        "Satisfaction": np.clip(np.random.normal(loc=70, scale=15, size=n_employees), 30, 100),
        "PerformanceScore": performance_score,
        "HoursWorked": hours_worked,
        "Age": np.random.randint(22, 60, size=n_employees),
    })

    # Sauvegarder le jeu de données pour réutilisation
    employee_data.to_csv("hr_analytics_demo.csv", index=False)
    print("\nJeu de données généré et sauvegardé dans hr_analytics_demo.csv")
    return employee_data


employee_data = load_employee_data(args.data) if args.data else generate_demo_data()

# Afficher un résumé du jeu de données
print("--- Aperçu du jeu de données ---")
print(employee_data.head())
print("\n--- Statistiques descriptives ---")
print(employee_data.describe(include='all'))

# Analyse descriptive
print("\n--- Moyennes par département ---")
print(employee_data.groupby("Department")[['PerformanceScore', 'HoursWorked', 'Satisfaction']].mean())

if "Segment" in employee_data.columns:
    print("\n--- Stats par segment ---")
    print(employee_data.groupby("Segment")[['PerformanceScore', 'HoursWorked', 'Satisfaction']].agg(['mean','median','std']))

# Visualisations
plt.figure(figsize=(12, 6))
sns.histplot(employee_data['PerformanceScore'], kde=True, bins=20, color='b')
plt.title('Distribution des scores de performance')
plt.xlabel('Performance Score')
plt.ylabel('Effectif')
plt.savefig('distribution_performance.png', dpi=150)
plt.close()

plt.figure(figsize=(12, 6))
sns.histplot(employee_data['HoursWorked'], kde=True, bins=20, color='g')
plt.title('Distribution des heures travaillées')
plt.xlabel('Hours Worked')
plt.ylabel('Effectif')
plt.savefig('distribution_hours.png', dpi=150)
plt.close()

plt.figure(figsize=(14, 6))
sns.boxplot(x='Department', y='PerformanceScore', data=employee_data, palette='Set2')
plt.title('Score de performance par département')
plt.xlabel('Département')
plt.ylabel('Performance Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('performance_by_department.png', dpi=150)
plt.close()

plt.figure(figsize=(14, 6))
sns.boxplot(x='Department', y='HoursWorked', data=employee_data, palette='Set3')
plt.title('Heures travaillées par département')
plt.xlabel('Département')
plt.ylabel('Hours Worked')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('hours_by_department.png', dpi=150)
plt.close()

# Détection d'outliers via IQR
q1 = employee_data['PerformanceScore'].quantile(0.25)
q3 = employee_data['PerformanceScore'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers_perf = employee_data[(employee_data['PerformanceScore'] < lower_bound) | (employee_data['PerformanceScore'] > upper_bound)]

print(f"\n--- Outliers PerformanceScore ({len(outliers_perf)}) ---")
print(outliers_perf[['EmployeeID', 'Department', 'PerformanceScore', 'HoursWorked', 'Satisfaction']])

q1_h = employee_data['HoursWorked'].quantile(0.25)
q3_h = employee_data['HoursWorked'].quantile(0.75)
iqr_h = q3_h - q1_h
lower_h = q1_h - 1.5 * iqr_h
upper_h = q3_h + 1.5 * iqr_h
outliers_hours = employee_data[(employee_data['HoursWorked'] < lower_h) | (employee_data['HoursWorked'] > upper_h)]

print(f"\n--- Outliers HoursWorked ({len(outliers_hours)}) ---")
print(outliers_hours[['EmployeeID', 'Department', 'PerformanceScore', 'HoursWorked', 'Satisfaction']])

# Corrélation
corr_columns = [c for c in ['PerformanceScore', 'HoursWorked', 'Satisfaction', 'Age'] if c in employee_data.columns]
corr = employee_data[corr_columns].corr()
print("\n--- Matrice de corrélation ---")
print(corr)

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matrice de corrélation')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=150)
plt.close()

print("\nVisualisations sauvegardées : distribution_performance.png, distribution_hours.png, performance_by_department.png, hours_by_department.png, correlation_matrix.png")

# Score de contribution
# Chaque critère est converti en rang centile (0-1) : robuste aux outliers et
# indépendant des unités (points, heures). Le score final est ramené sur 100.
employee_data["Efficacite"] = employee_data["PerformanceScore"] / employee_data["HoursWorked"]
criteria = {
    "Performance": employee_data["PerformanceScore"],
    "Efficacite": employee_data["Efficacite"],
    "Satisfaction": employee_data["Satisfaction"],
}
employee_data["ScoreContribution"] = 100 * sum(
    SCORE_WEIGHTS[name] * values.rank(pct=True) for name, values in criteria.items()
)

ranking = employee_data.sort_values("ScoreContribution", ascending=False).reset_index(drop=True)
ranking.index = ranking.index + 1
ranking.index.name = "Rang"
top = ranking.head(args.top)

weights_label = ", ".join(f"{name} {int(w * 100)}%" for name, w in SCORE_WEIGHTS.items())
print(f"\n--- Top {len(top)} des employés par score de contribution ({weights_label}) ---")
print(top[["EmployeeID", "Department", "PerformanceScore", "HoursWorked", "Efficacite", "Satisfaction", "ScoreContribution"]]
      .round(2).to_string())

best = ranking.iloc[0]
print(
    f"\nEmployé le plus contributif : n°{best['EmployeeID']} ({best['Department']}), "
    f"score {best['ScoreContribution']:.1f}/100 : performance {best['PerformanceScore']:.0f}, "
    f"{best['HoursWorked']:.0f} h/semaine, satisfaction {best['Satisfaction']:.0f}."
)

ranking.to_csv("classement_employes.csv")

plt.figure(figsize=(12, 6))
labels = [f"#{eid} ({dep})" for eid, dep in zip(top["EmployeeID"], top["Department"])]
sns.barplot(x=top["ScoreContribution"].values, y=labels, color="#45a3e6")
plt.title(f"Top {len(top)} des employés par score de contribution")
plt.xlabel("Score de contribution (0-100)")
plt.ylabel("Employé")
plt.xlim(0, 100)
plt.tight_layout()
plt.savefig("top_employes.png", dpi=150)
plt.close()

print("Classement complet : classement_employes.csv · graphique : top_employes.png")
