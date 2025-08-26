# 💵 Répartition Flux – 60% / 25% / 15%

### 🧭 Description

Application locale en **Python (Tkinter)** permettant de répartir automatiquement un montant en trois postes financiers :

* **Revenu 60%**
* **Épargne 25%**
* **Réserve 15%**

Chaque opération est enregistrée dans un fichier CSV local, sans base de données ni dépendance extérieure.
Pensée pour un usage **minimaliste, portable, et autonome**.

---

### 💠 Fonctionnalités

* Entrée d’un montant (arrondi automatiquement a l'unité "0" ou "5" les plus proches)
* Répartition automatique selon le schéma **60/25/15**
* Stockage dans trois fichiers CSV (`revenu.csv`, `épargne.csv`, `réserve.csv`)
* Vue directe des **totaux cumulés** et du **dernier ajout** par poste via un `Treeview`
* **Couleurs de ligne** distinctes par poste :

  * Revenu → bleu clair
  * Épargne → violet clair
  * Réserve → orange clair
* Interface simple, légère, sans dépendance externe

---

### 📁 Arborescence des fichiers

Lors de la première exécution, le programme crée automatiquement cette structure :

```
/ton_dossier/
├── repartition_caisse.py
├── README.md
└── data/
    ├── revenu.csv
    ├── épargne.csv
    └── réserve.csv
```

Tous les fichiers sont stockés **dans le dossier `data/` à côté du script**.
Aucune dépendance à un chemin personnel.

---

### ⚙️ Utilisation

1. Lancer `repartition_caisse.py`
2. Entrer un **montant** (XPF, entier uniquement)
3. Cliquer sur **Répartir & Enregistrer**
4. Consulter la répartition et les totaux dans le tableau
5. Utiliser le bouton **Recharger les totaux** si besoin

Exemple d’affichage :

```
Poste        | Dernier + | Total cumulé
-------------|-----------|-------------
Revenu 60%   | 6000      | 120000
Épargne 25%  | 2500      | 50000
Réserve 15%  | 1500      | 30000
```

---

### 📄 Format des données CSV

* En-tête : `date,montant`
* Exemple :

```
date,montant
2025-08-26 14:05:03,6000
2025-08-26 14:05:03,2500
2025-08-26 14:05:03,1500
```

---

### 🔐 Licence

repartition\_flux - **Licence Libre avec Clause Commerciale**
Copyright © 2025 **DEV\_SASHOTUA** – Tous droits réservés.

Ce programme est publié sous **Licence GNU GPL v3**, avec une clause additionnelle restreignant l’usage commercial **sans autorisation**.

Vous êtes autorisé à :

* utiliser, modifier, distribuer le code à des fins personnelles ou éducatives.

Vous n’êtes **pas autorisé** à :

* utiliser ce programme à des fins commerciales (vente, intégration, prestation) sans accord écrit de l’auteur.

Texte complet : http://www.gnu.org/licences/gpl-3.0.html

---

### 👤 Auteur

* **DEV\_SASHOTUA**
  📩 Contact : sashotua_dev@proton.me

---

### 🆔 Version

* `/001` – 26 août 2025
