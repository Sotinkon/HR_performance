"""
Projet 2 : Explorer et comprendre les performances des employés
Python / pandas / seaborn

Objectif : étudier les distributions des scores de performance et des heures travaillées,
identifier des outliers et visualiser les tendances.

Ce script génère un dataset de démonstration si aucun jeu de données n'est fourni,
mais il peut facilement être adapté à un dataset réel HR Analytics.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

# Génération d'un jeu de données d'exemple
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

# Afficher un résumé du jeu de données
print("--- Aperçu du jeu de données ---")
print(employee_data.head())
print("\n--- Statistiques descriptives ---")
print(employee_data.describe(include='all'))

# Sauvegarder le jeu de données pour réutilisation
employee_data.to_csv("hr_analytics_demo.csv", index=False)
print("\nJeu de données généré et sauvegardé dans hr_analytics_demo.csv")

# Analyse descriptive
print("\n--- Moyennes par département ---")
print(employee_data.groupby("Department")[['PerformanceScore', 'HoursWorked', 'Satisfaction']].mean())

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
corr = employee_data[['PerformanceScore', 'HoursWorked', 'Satisfaction', 'Age']].corr()
print("\n--- Matrice de corrélation ---")
print(corr)

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matrice de corrélation')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=150)
plt.close()

print("\nVisualisations sauvegardées : distribution_performance.png, distribution_hours.png, performance_by_department.png, hours_by_department.png, correlation_matrix.png")
