import streamlit as st
from Optimac_API import add_participant, add_feedback

st.title("Campagne fictive d'action participative")

if "count" not in st.session_state:
    st.session_state.count = 0

if "constants" not in st.session_state :
    st.session_state["constants"] = {}
    if "scale" not in st.session_state["constants"] : 
        st.session_state["constants"]["scale"] = [
            "Pas du tout",
            "Non",
            "Plutôt non",
            "Neutre/ne sais pas",   
            "Plutôt oui",
            "Oui",
            "Tout à fait",
        ]

    if "motiv_map" not in st.session_state["constants"]:
        scale = st.session_state["constants"]["scale"]
        st.session_state["constants"]["motiv_map"] = {scale[i]:i-3 for i in range(len(scale))}

    if "meaningful" not in st.session_state["constants"]:
        st.session_state["constants"]["meaningful"] =  {"weekly":"placer des graines une fois par semaine",
                "monthly":"placer des graines une fois par mois",
                "notatall":"ne pas placer de graines"}

if "res" not in st.session_state:
    st.session_state["res"] = []

"Étape :", st.session_state.count+1,"/3" 

if st.session_state.count == 0:
    st.markdown("""
    blabla

    """)

    motivations = {"weekly":0, "monthly":0,"notatall":0} 
    meaningful = st.session_state["constants"]["meaningful"] 
    motiv_map = st.session_state["constants"]["motiv_map"]
    with st.form("action_motivations"):
        for action in motivations:
            motivation_string = st.select_slider(
                f"Voudriez-vous {meaningful[action]} ?",
                options=st.session_state["constants"]["scale"])
            motivations[action] = motiv_map[motivation_string]

        submitted = st.form_submit_button("Soumettre") 
        if submitted:
            with st.spinner("Traitement de vos réponses en cours...", show_time=True):
                st.session_state["res"] = add_participant(motivations)
                st.session_state.count+=1

if st.session_state.count == 1 :
    res = st.session_state["res"]
    meaningful = st.session_state["constants"]["meaningful"] 
    st.markdown(f"""
Nous vous proposons d'éffectuer l'action suivante {meaningful[res[1]]}.\n
Si nous vous demandions de l'appliquer dans votre quotidien, le feriez vous ?
                """)
    with st.form("feedback"):
        selected_feedback = st.feedback("thumbs")
        if st.form_submit_button("Soumettre",type="primary",key=1):
            if selected_feedback is not None:
                with st.spinner("Traitement de votre réponse en cours...", show_time=True):
                    add_feedback(list(res), selected_feedback)
                st.markdown("Merci pour vos réponses et votre participation à cette expérience, vous pouvez fermer cet onglet")
