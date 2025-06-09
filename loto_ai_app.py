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
    tirages = recuperer_tirages_loto()
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
