import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import random
from collections import Counter

@st.cache_data(show_spinner=False)
def recuperer_tirages_loto(n=50):
    url = "https://tirage-gagnant.com/resultats-loto/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    blocs = soup.find_all("div", class_="results")[:n]
    tirages = []
    for bloc in blocs:
        boules = bloc.find_all("span", class_="boule")
        nums = [int(b.text.strip()) for b in boules if b.text.strip().isdigit()]
        if len(nums) >= 5:
            tirages.append(nums[:5])
    return tirages

def calcul_stats(tirages):
    flat = [num for tirage in tirages for num in tirage]
    freq = Counter(flat)
    stats = {}
    for num in range(1, 50):
        stats[num] = {
            "frequence": freq.get(num, 0),
            "retard": next((i for i, tir in enumerate(reversed(tirages)) if num in tir), len(tirages))
        }
    return stats

def generer_grille(stats, total=5):
    poids = []
    for num in range(1, 50):
        s = stats[num]
        score = s["frequence"] * 1.5 + s["retard"] * 1.0
        poids.append(score)
    probs = np.array(poids) / sum(poids)
    return sorted(np.random.choice(np.arange(1, 50), size=5, replace=False, p=probs))

def generer_grille_euromillions():
    base = sorted(random.sample(range(1, 51), 5))
    etoiles = sorted(random.sample(range(1, 13), 2))
    return base, etoiles

# Interface Streamlit
st.title("🔮 Pronostics Loto & EuroMillions (IA légère)")
try:
 try:
    tirages = recuperer_tirages_loto()
    if not tirages or len(tirages) < 10:
        raise ValueError("Pas assez de tirages récupérés.")
except:
    st.warning("Tirages non récupérables en ligne. Utilisation de données locales.")
    tirages = [
        [7, 30, 37, 40, 45],
        [5, 12, 27, 30, 44],
        [11, 22, 24, 37, 45],
        [9, 21, 30, 37, 42],
        [3, 12, 24, 35, 45],
        [6, 19, 24, 30, 38],
        [1, 14, 17, 30, 37],
        [12, 24, 28, 32, 45],
        [4, 7, 24, 36, 37],
        [2, 5, 30, 34, 42],
        [15, 16, 30, 31, 45],
        [8, 12, 24, 33, 37],
        [13, 18, 20, 24, 30],
        [19, 24, 27, 30, 45],
        [10, 24, 30, 39, 43]
    ]

# Toujours exécuté, que ce soit depuis le scraping ou le fallback
stats = calcul_stats(tirages)




    stats = calcul_stats(tirages)

    if st.button("🎰 Générer grille Loto IA"):
        grille = generer_grille(stats)
        chance = random.randint(1, 10)
        st.success(f"Numéros : {grille} | Chance : {chance}")

    if st.button("⭐ Générer grille EuroMillions"):
        base, etoiles = generer_grille_euromillions()
        st.success(f"Numéros : {base} | Étoiles : {etoiles}")
except Exception as e:
    st.error("Erreur lors du chargement des données. Vérifiez votre connexion internet.")
