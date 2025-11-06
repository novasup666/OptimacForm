import streamlit as st
from Optimac_API import add_participant

st.title("Campagne fictive d'action participative")

st.markdown("""
blabla

""")

scale=[
    "Pas du tout",
    "Non",
    "Plutôt non",
    "Neutre/ne sais pas",   
    "Plutôt oui",
    "Oui",
    "Tout à fait",
]

motiv_map = {scale[i]:i-3 for i in range(len(scale))}
meaningful = {"weekly":"placer des graines une fois par semaine",
             "monthly":"placer des graines une fois par mois",
             "notatall":"ne pas placer de graines"}   
motivations = {"weekly":0, "monthly":0,"notatall":0} 

for action in motivations:
    motivation_string = st.select_slider(
        f"Voudriez-vous {meaningful[action]} ?",
        options=scale)
    motivations[action] = motiv_map[motivation_string]

if st.button("Soumettre",type="primary"):
    res = add_participant(motivations)
else:
    res= None
res