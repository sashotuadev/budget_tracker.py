#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv, os

# === CHEMINS (portables, neutres) ===
BASE_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(BASE_DIR, exist_ok=True)

FILES = {
    "Revenu 60%":  os.path.join(BASE_DIR, "revenu.csv"),
    "Épargne 25%": os.path.join(BASE_DIR, "épargne.csv"),
    "Réserve 15%": os.path.join(BASE_DIR, "réserve.csv"),
}

FIELDNAMES = ["date", "montant"]  # colonnes uniformes

# === INIT CSV avec entêtes si absent ===
for path in FILES.values():
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(FIELDNAMES)

# === LOGIQUE RÉPARTITION ===
def repartir_xpf(montant_xpf: int) -> dict:
    """
    Retourne un dict {poste: montant} en 60/25/15,
    avec “Réserve” ajustée pour compenser l'arrondi.
    """
    revenu   = int(montant_xpf * 0.60)
    epargne  = int(montant_xpf * 0.25)
    reserve  = montant_xpf - revenu - epargne
    return {"Revenu 60%": revenu, "Épargne 25%": epargne, "Réserve 15%": reserve}

def arrondi_5_xpf(val: int) -> int:
    """Arrondi à 5 (entier)."""
    return int(round(val / 5.0) * 5)

# === CUMULS ===
def totaliser(path: str) -> int:
    """Somme la colonne 'montant' d'un CSV."""
    total = 0
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    total += int(row["montant"])
                except Exception:
                    continue
    return total

def ecrire_ligne(path: str, date_str: str, montant: int) -> None:
    """Append d'une ligne date/montant dans un CSV existant."""
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        # Pas de writeheader ici: déjà écrit à l'init
        writer.writerow({"date": date_str, "montant": montant})

# === UI ===
class App:
    def __init__(self, root):
        self.root = root
        root.title("Répartition Flux– Simple (60%-25%-15%)")
        root.geometry("520x460")

        # Entrée Montant
        top = tk.Frame(root)
        top.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(top, text="Montant :").pack(anchor="w")
        self.montant_var = tk.StringVar()
        tk.Entry(top, textvariable=self.montant_var).pack(fill=tk.X)

        # Boutons
        btns = tk.Frame(root)
        btns.pack(fill=tk.X, padx=10, pady=6)

        tk.Button(btns, text="Répartir & Enregistrer", command=self.repartir_enregistrer, background="red", foreground="white").pack(side=tk.BOTTOM, padx=4)


        # Treeview (vue directe)
        mid = tk.Frame(root)
        mid.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        self.tree = ttk.Treeview(mid, columns=("poste","dernier","total"), show="headings", height=6)
        self.tree.heading("poste", text="Poste")
        self.tree.heading("dernier", text="Dernier + ")
        self.tree.heading("total", text="Total cumulé ")
        self.tree.column("poste", width=140, anchor="w")
        self.tree.column("dernier", width=160, anchor="e")
        self.tree.column("total", width=180, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(mid, text="Recharger les totaux", command=self.mettre_a_jour_vue).pack(side=tk.LEFT, padx=4)

        # Statut
        self.statut = tk.StringVar()
        tk.Label(root, textvariable=self.statut, fg="green").pack(pady=4)

        # Pied de page
        footer = tk.Label(
            root,
            text="© DEV_SASHOTUA - VERSION /001 - 26 août 2025 - License GPL GNU v3",
            font=("Arial", 8),
            fg="gray"
        )
        footer.pack(side="bottom", pady=4)

        # Charge la vue au démarrage
        self.mettre_a_jour_vue()

    def repartir_enregistrer(self):
        # 1) Lire et valider le montant
        brut = self.montant_var.get().strip()
        if not brut:
            messagebox.showwarning("Saisie", "Veuillez entrer un montant.")
            return
        try:
            val = int(brut)
        except ValueError:
            messagebox.showerror("Entrée invalide", "Le montant doit être un entier .")
            return

        val = arrondi_5_xpf(val)
        if val <= 0:
            messagebox.showerror("Montant", "Le montant doit être > 0.")
            return

        # 2) Répartir
        parts = repartir_xpf(val)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 3) Écrire les trois lignes, puis recharger
        for poste, montant in parts.items():
            ecrire_ligne(FILES[poste], date_str, montant)

        self.montant_var.set("")
        self.statut.set(f"Répartition enregistrée: Revenu {parts['Revenu 60%']} | Épargne {parts['Épargne 25%']} | Réserve {parts['Réserve 15%']}")
        self.mettre_a_jour_vue()

    def mettre_a_jour_vue(self):
        """Recharge le Treeview avec (dernier ajout estimé=0) + totaux;
        remplacé par la dernière répartition si disponible via lecture de fin de fichiers."""
        # On va chercher les totaux et déduire le dernier ajout (facultatif).
        self.tree.delete(*self.tree.get_children())

        # Pour afficher le "dernier +", on lit la dernière ligne de chaque fichier (si elle existe)
        def dernier_ajout(path: str) -> int:
            if not os.path.exists(path):
                return 0
            try:
                with open(path, "r", encoding="utf-8") as f:
                    rows = list(csv.DictReader(f))
                    if not rows:
                        return 0
                    return int(rows[-1]["montant"])
            except Exception:
                return 0

        lignes = []
        for poste, path in FILES.items():
            total = totaliser(path)
            dernier = dernier_ajout(path)
            lignes.append((poste, dernier, total))

        # Injection dans le Treeview
                # Injection dans le Treeview avec couleurs
        for poste, dernier, total in lignes:
            if poste == "Revenu 60%":
                tag = "revenu"
            elif poste == "Épargne 25%":
                tag = "epargne"
            else:
                tag = "reserve 15%"
            self.tree.insert("", tk.END, values=(poste, f"{dernier}", f"{total}"), tags=(tag,))

        # Définition des styles de tags (couleurs de fond)
        self.tree.tag_configure("revenu", background="#e6f7ff")   # bleu clair
        self.tree.tag_configure("epargne", background="#f9f0ff") # violet clair
        self.tree.tag_configure("reserve", background="#fff7e6") # orange clair

        # Label statut court
        self.statut.set("Totaux rechargés.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
