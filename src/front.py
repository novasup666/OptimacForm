import streamlit as st
from time import time
import random as rd
from config import meaningful
#from Optimac_API import add_participant, add_feedback

st.title("Campagne d'opinion: Action participative")

if "count" not in st.session_state:
    st.session_state.count = 0


if "scale" not in st.session_state : 
    st.session_state["scale"] = [
        "Pas du tout",
        "Non",
        "Plutôt non",
        "Neutre/ne sais pas",   
        "Plutôt oui",
        "Oui",
        "Tout à fait",
    ]

if "motiv_map" not in st.session_state:
    scale = st.session_state["scale"]
    st.session_state["motiv_map"] = {scale[i]:i-3 for i in range(len(scale))}


if "seed" not in st.session_state:
    st.session_state["seed"] = time()

"Étape :", st.session_state.count+1,"/3" 

if st.session_state.count == 0:
    st.markdown("""
    Le projet OPTIMAC est mené par l'équipe DRUID de l'IRISA. Son objectif est de fournir des outils pour la mise en place de campagnes d'action participatives. Ces campagnes ont la particularité de faire participer les citoyens à la production de données scientifiques au travers de la réalisation concrète d'expériences. Par exemple: tondre son gazon à une certaine fréquence (ex 1fois/semaine) et tenir compte de l'évolution de la biodiversité.
    Au sein du projet optimac nous essayons de modéliser le comportement de participants à de telles campagnes pour pouvoir affiner la méthode avec laquelle attribuer les expériences aux participants.
    Ainsi, vous allez participer à deux campagnes fictives:

    D'abord: disons que vous ayez un jardin : quelle fréquence de tonte seriez vous d'accord d'adopter le temps d'une expérience d'un mois (avec prise de mesures de biodiversité).

    Ensuite: à quelle fréquence seriez vous prêts à placer de la nourriture pour oiseaux au bords de votre fenetre (et de réaliser des mesures de biodiversité) au cours d'un mois.

    Vous allez devoir juger les différentes propositions, nous vous demandons de le faire le plus honnètement possible, en essayant de vous projeter. N'hésitez pas à prendre votre temps!
    Ensuite vous vous verrez attribué une action et nous vous demanderons d'indiquer si vous penser que vous mettriez vraiment cette action en place ou si vous pensez que vous n'arriverez pas à vous y tenir. De la même façon, soyez le plus honnête et n'hésitez pas à prendre votre temps.
    """)

    motivations = {"weekly":0, "monthly":0,"notatall":0} 
    motiv_map = st.session_state["motiv_map"]
    with st.form("action_motivations"):
        for action in motivations:
            motivation_string = st.segmented_control(
                f"Voudriez-vous {meaningful[action]} ?",
                options=st.session_state["scale"], 
                selection_mode="single")
            motivations[action] = motiv_map[motivation_string]

        submitted = st.form_submit_button("Soumettre") 
        if submitted:
            with st.spinner("Traitement de vos réponses en cours...", show_time=True):
                st.session_state["res"] = add_participant(motivations)
                st.session_state.count+=1
                st.rerun()

if st.session_state.count == 1 :
    res = st.session_state["res"]
    with st.form("feedback"):
        st.markdown(f"""
Nous vous proposons d'éffectuer l'action suivante: "{meaningful[res[1]]}".\n
Si nous vous demandions de l'appliquer dans votre quotidien, le feriez vous ?
                """)
        selected_feedback = st.feedback("thumbs")
        if st.form_submit_button("Soumettre",type="primary",key=1):
            if selected_feedback is not None:
                with st.spinner("Traitement de votre réponse en cours...", show_time=True):
                    add_feedback(list(res), selected_feedback)
                    st.session_state.count+=1
                    st.rerun()
if st.session_state.count ==2:
    st.markdown("Merci pour vos réponses et votre participation à cette expérience, vous pouvez fermer cet onglet.")

#sdlf<sdmf