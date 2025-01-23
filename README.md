# Application de QCM pour Étudiants en Informatique

Bienvenue dans l'application de QCM conçue pour les étudiants en informatique ! Cette application permet de répondre à des questionnaires à choix multiples, de suivre vos scores, et même d'ajouter vos propres questions (pour les administrateurs).

## Fonctionnalités principales

- **Gestion des utilisateurs** :
  - Création automatique d'un profil utilisateur.
  - Suivi de l'historique des tests avec date, catégorie et scores.
- **Gestion des questions** :
  - Organisation par catégories (Python, Réseaux, Algorithmes, etc.).
  - Possibilité d'ajouter des questions pour les administrateurs.
- **Feedback immédiat** :
  - Indique si une réponse est correcte ou incorrecte.
  - Affiche la bonne réponse en cas d'erreur.
- **Exportation des résultats** :
  - Génération d'un fichier CSV avec les scores et les détails des tests.

## Prérequis

- Python 3.7 ou supérieur.
- Bibliothèques Python incluses : `json`, `os`, `datetime`.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/locoDZ/AP_Projet.git
   ```
2. Assurez-vous que les fichiers `users.json` et `questions.json` sont dans le même dossier que le script Python.

## Lancement de l'application

1. Exécutez le script principal :
   ```bash
   python projetAP.py
   ```
2. Saisissez votre nom d'utilisateur.
   - Si vous êtes un nouvel utilisateur, un profil sera créé automatiquement.
3. Suivez les instructions à l'écran pour choisir une catégorie ou une action.

## Exemple d'exécution

### Utilisateur standard

- Lancer l'application et saisir un nom d'utilisateur :

  ```text
  Welcome to the Computer Science MCQ!

  Enter your username: Aziz

  Welcome back, Aziz!
  Available options:
  1. Python
  2. Algorithms
  3. Network
  4. Software Engineering
  5. Databases
  6. OOP
  7. AI
  8. Cybersecurity
  9. All Categories
  10. View History
  11. Export Results
  12. Exit

  You can select an option by entering either:
  - The number (e.g., '1')
  - The category name (e.g., 'Python')
  - Commands: 'all', 'history', 'export', 'exit'

  Enter your choice: 

  Starting quiz for category: Python

   Question 1: What is the data type in Python used to represent text?
   a) int
   b) str
   c) list
   Answer: b
   Correct!
  ```

- À la fin du test :

  ```text
   Your final score: 5/5
  ```

### Administrateur

- Ajouter une nouvelle question :
  ```text
  Adding Questions:

  Available categories:
  1. Python
  2. Algorithms
  3. Network
  4. Software Engineering
  5. Databases
  6. OOP
  7. AI
  8. Cybersecurity

  Select a category by number:8

  Adding a new question to the category: Cybersecurity
  Enter the question: Which protocol is commonly used to securely transfer files over a network?
  Enter option a: FTP
  Enter option b: SFTP
  Enter option c: Telnet
  Enter the correct answer (a, b, or c): b

  Question added successfully!
  Do you want to add another question? (yes/no):  
  
  ```

## Exportation des résultats

Pour exporter vos résultats en CSV :

1. Sélectionnez l'option "Export Results" dans le menu.
2. Un fichier `nom_utilisateur_results.csv` sera créé dans le dossier courant.

  ```text
    Date,Score,Total Questions,Category
    2024-12-31,3,4,All
    2024-12-31,11,16,All

  ```

Profitez de l'application et amusez-vous à apprendre !

