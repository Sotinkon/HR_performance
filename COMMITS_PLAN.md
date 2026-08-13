# Plan de Commits Détaillés - Projet 2 HR Performance

## Phase 1 : Infrastructure (5 commits)
1. docs: Create initial project structure and README skeleton
2. chore: Add Python venv setup and requirements.txt with core dependencies
3. chore: Configure venv activation scripts and environment setup
4. docs: Add project objectives and problem statement
5. chore: Initialize git repository and add .gitignore

## Phase 2 : Imports et Configuration (3 commits)
6. feat: Add numpy and pandas imports for data manipulation
7. feat: Add matplotlib and seaborn for visualization and statistical plotting
8. feat: Configure seaborn style and set random seed for reproducibility

## Phase 3 : Génération de Données (8 commits)
9. feat: Generate synthetic employee dataset with 200 records
10. feat: Create realistic performance score distribution (mean=70, std=12)
11. feat: Create hours worked distribution (mean=42, std=5)
12. feat: Add department classification with realistic proportions
13. feat: Add seniority segments (Junior, Mid, Senior)
14. feat: Add age range and satisfaction score to employee data
15. feat: Inject intentional outliers for anomaly detection practice
16. feat: Export generated dataset to CSV format (hr_analytics_demo.csv)

## Phase 4 : Analyse Descriptive (7 commits)
17. feat: Display dataset overview with head() and basic info
18. feat: Calculate and display descriptive statistics (mean, median, std, quartiles)
19. feat: Implement group-by analysis for department performance metrics
20. feat: Implement group-by analysis for seniority segment comparison
21. feat: Calculate correlation matrix for variable relationships
22. docs: Add explanation of descriptive statistics concepts (mean, median, IQR)
23. docs: Document outlier detection methodology using IQR rule

## Phase 5 : Visualisations (7 commits)
24. feat: Create histogram with KDE for performance score distribution
25. feat: Create histogram with KDE for hours worked distribution
26. feat: Generate boxplot for performance scores by department
27. feat: Generate boxplot for hours worked by department
28. feat: Implement correlation matrix heatmap visualization
29. feat: Add outlier detection and filtering logic
30. feat: Print identified outliers and anomaly summary statistics

## Phase 6 : Optimisation et Tests (3 commits)
31. refactor: Add comments and docstrings to main analysis functions
32. test: Verify dataset generation reproducibility with seed
33. docs: Create inline documentation for data transformations

## Phase 7 : Documentation - Stack Technique (3 commits)
34. docs: Add stack technique section with library roles table
35. docs: Document NumPy concepts and numerical operations
36. docs: Document Pandas DataFrame manipulation and operations

## Phase 8 : Documentation - Guide d'Exécution (4 commits)
37. docs: Create comprehensive venv setup guide with step-by-step instructions
38. docs: Document installation and dependency management workflow
39. docs: Explain Python script execution step-by-step with code examples
40. docs: Add file generation and output documentation

## Phase 9 : Documentation - Concepts et Datasets (3 commits)
41. docs: Add detailed explanation of statistical concepts (distribution, outliers)
42. docs: Document HR Analytics Dataset source and column meanings
43. docs: Add dataset sources links (Kaggle, UCI ML Repository, GitHub)

## Final Phase : Integration et Polish (1 commit)
44. docs: Final README review, add table of contents and links

Total : 44 commits stratégiques et documentés
