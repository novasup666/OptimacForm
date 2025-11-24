import streamlit as st
from time import time
import random as rd
from config import meaningful_actions, verbose
from form_API import add_participant,add_motivations, add_feedback, add_suggestion

st.title("Campagne d'opinion: action participative")

if "count" not in st.session_state:
    st.session_state.count = 0


if "scale" not in st.session_state : 
    st.session_state["scale"] = [
        "Absolument pas",
        "Non",
        "Plutôt non",
        "Ne sais pas",   
        "Plutôt oui",
        "Oui",
        "Oui, absolument",
    ]

if "smaller_scale" not in st.session_state : 
    st.session_state["smaller_scale"] = [
        "Non",
        "Oui, mais pas sûr",
        "Oui",
    ]

if "motiv_map" not in st.session_state:
    scale = st.session_state["scale"]
    st.session_state["motiv_map"] = {scale[i]:i-3 for i in range(len(scale))}


if "actions" not in st.session_state:
    rd.seed(time())
    actions = [[action for action in meaningful] for meaningful in meaningful_actions]
    for l in actions:
        l.sort(key=(lambda x: (rd.random(),x)))
    st.session_state["actions"] = actions

if "i" not in st.session_state:
    st.session_state["i"] = 0

if "feedbacks" not in st.session_state:
    st.session_state["feedbacks"] = {}

if "campaign_id" not in st.session_state:
    st.session_state["campaign_id"] = 0

if "nb_campaigns" not in st.session_state:
    st.session_state["nb_campaigns"] = len(verbose)

if "finished" not in st.session_state:
    st.session_state["finished"] = False

"Étape :", st.session_state.count+1,"/3" 

if st.session_state.count == 0:
    #Introduction page
    st.markdown("""
    Le projet OPTIMAC est mené par l'équipe DRUID de l'IRISA. Son objectif est de fournir des outils pour la mise en place de campagnes d'action participatives. 

    Ces campagnes ont la particularité de faire participer les citoyens à la production de données scientifiques au travers de la réalisation concrète d'expériences. Par exemple: tondre son gazon à une certaine fréquence (ex 1fois/semaine) et tenir compte de l'évolution de la biodiversité dans le dit jardin.
    L'une des tâches du projet Optimac est de modéliser le comportement de participants à de telles campagnes pour pouvoir affiner la méthode avec laquelle attribuer ces expériences aux participants.
    
    Ainsi, vous allez participer à deux campagnes fictives qui seront détaillées plus loin. 

    Pas d'inquiétude ! Vous n'avez besoin que de 5 minutes pour remplir ce formulaire (et même pas besoin de jardin !).

    Avant de commencer, petit point données personnelles: 
    - Nous avons besoin de collecter quelques informations personnelles à des fins statistiques. 
    - Nous vous informons que nous ne collectons que les données que vous fournirez dans ce formulaire.
    - Toute réponse soumise à ce formulaire est hébergée par Google et donc potentiellement en dehors de l'Union Européenne. 
    - La soumission du formulaire suivant vaut pour acceptation du stockage de ces données sur les serveurs de GOOGLE et de leurs exploitation pleine et entière par les membres présents et futurs de l'équipe DRUID de l'IRISA. 

    """)
    
    with st.form("Preliminary informations"):
        age = st.radio("Indiquez votre catégorie d'âge:",
        [   "entre 18 et 25 ans",
            "entre 26 et 40 ans",
            "entre 41 et 65 ans",
            "66 ans et plus"])
        gender = st.radio("Précisez votre genre :",
        [   "Feminin",
            "Masculin",
            "Mon genre n'est pas répertorié."])
        social_category = st.radio("Indiquez votre catégorie socio-professionnelle (échelle PCS2003):",
        [   "Agriculteurs/agricultrices exploitant.e.s",
            "Artisan.e.s, commerçant.e.s et chef.fe.s d'entreprise",
            "Cadres et professions intellectuelles supérieures",
            "Professions intermédiaires",
            "Employé.e.s",
            "Ouvrier.e.s",
            "Retraité.e.s",
            "Autres personnes sans activités professionnelles (dont militaires, étudiant.e.s)"
        ])

        self_eval = st.radio("Comment évalueriez votre niveau d'expertise en biologie/écologie/biodiversité ?",
        [   "Expert.e : Vous travaillez dans le domaine de la biologie, écologie",
            "Connaisseur.euse : Vous êtes sensible à ces sujets et avez suivi des formations/stages à ce propos",
            "Amateur.e : Vous êtes sensible à ces sujets mais avez suivi une formation peu conséquente",
            "Novice: Vous n'avez pas de connaissances particulières sur le sujet"])
        
        submitted = st.form_submit_button("Soumettre",type="primary",key=0)

        if submitted and [age,gender,social_category,self_eval]!=[None,None,None,None]:
            with st.spinner("Traitement de vos réponses en cours...", show_time=True):
                st.session_state["n"] = add_participant(age,gender,social_category,self_eval)
                st.session_state.count +=1
                st.rerun()
        elif submitted:
            "Pour continuer il est nécessaire de remplir l'intégralité des questions ci-dessus."

if st.session_state.count >= 1:
    c_id = st.session_state["campaign_id"]
if st.session_state.count == 1:
    #
    st.markdown(verbose[st.session_state["campaign_id"]])
    motivations = {} 
    motiv_map = st.session_state["motiv_map"]
    with st.form("action_motivations"):
        for action in meaningful_actions[c_id]:
            motivation_string = st.segmented_control(
                f"Voudriez-vous {meaningful_actions[c_id][action]} ?",
                options=st.session_state["scale"], 
                selection_mode="single")
            if motivation_string is not None:
                motivations[action] = motiv_map[motivation_string]

        submitted = st.form_submit_button("Soumettre",type="primary",key=0)
        
        if submitted and len(motivations) == len(meaningful_actions[c_id]):
            with st.spinner("Traitement de vos réponses en cours...", show_time=True):
                add_motivations(c_id,st.session_state["n"],motivations)
                st.session_state["motivations"] = motivations
                st.session_state.count+=1
                st.rerun()
        elif submitted:
            "Completez toutes les questions du questionnaire s'il vous plaît."


if st.session_state.count >= 2 and st.session_state.count <2+len(st.session_state["actions"][c_id]):
    if st.session_state.count == 2+st.session_state["i"]:
        with st.form("feedback"):
            action = st.session_state["actions"][c_id][st.session_state["i"]]
            st.markdown(f"""
Supposons, qu'après avoir consulté l'avis que vous avez exprimé sur chaque actions, les organisateurs de l'experience vous demandent d'éffectuer l'action suivante: {meaningful_actions[c_id][action]}.
                    """)
            feedback = st.segmented_control(
                f"Pensez-vous que vous la réaliseriez du mieux possible ?",
                options=st.session_state["smaller_scale"], 
                selection_mode="single")
            if feedback is not None:
                st.session_state["feedbacks"][action] = feedback
            submitted = st.form_submit_button("Soumettre",type="primary",key=1) 

            if submitted and feedback is not None and st.session_state.count == 1+len(st.session_state["actions"][c_id]):
                with st.spinner("Traitement de votre réponse en cours...", show_time=True):
                    add_feedback(c_id,st.session_state["n"],st.session_state["motivations"], st.session_state["feedbacks"])
                    st.session_state.count+=1
                    st.rerun()
            elif submitted and feedback is not None:
                st.session_state.count+=1
                st.session_state["i"]+=1
                st.cache_data.clear()
                st.rerun()
            elif submitted:
                "Completez toutes les questions du questionnaire s'il vous plaît."

if st.session_state.count ==2+len(st.session_state["actions"][st.session_state["campaign_id"]]):
    if c_id< st.session_state["nb_campaigns"]-1:
        st.session_state["campaign_id"]+=1
        st.session_state.count = 1
        st.session_state["i"] = 0
        st.rerun()
    else: 
        with st.form("final_opinions"): 
            st.markdown("Merci pour vos réponses et votre participation à cette expérience.")
            suggestion = st.text_area("Vous pouvez fermer cet onglet ou nous donner vos suggestions ou votre avis sur cette campagne:")
            submitted = st.form_submit_button("Soumettre")
            if submitted:
                add_suggestion(st.session_state["n"], suggestion)
                st.session_state["finished"] = True

if st.session_state["finished"]:
    "Merci d'avoir partagé votre avis, vous pouvez fermer cet onglet"