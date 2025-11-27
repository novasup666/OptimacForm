import streamlit as st
from time import time
import random as rd
from config import meaningful_actions, verbose,presentation,verbose_feedback,campaign_names
from form_API import add_participant,add_motivations, add_feedback, add_suggestion

#>>> Initialisation of the constants in the session state
def init_sess_state(key,value):
    if key not in st.session_state:
        st.session_state[key] = value

init_sess_state("count",0)
init_sess_state("scale",[
        "Absolument pas",
        "Non",
        "Plutôt non",
        "Ne sais pas",   
        "Plutôt oui",
        "Oui",
        "Oui, absolument",
    ] )

init_sess_state( "smaller_scale" , [
        "Non",
        "Oui, mais pas sûr",
        "Oui",
    ])

if "motiv_map" not in st.session_state:
    scale = st.session_state["scale"]
    st.session_state["motiv_map"] = {scale[i]:i-3 for i in range(len(scale))}


if "actions" not in st.session_state:
    rd.seed(time())
    actions = [[action for action in meaningful] for meaningful in meaningful_actions]
    for l in actions:
        l.sort(key=(lambda x: (rd.random(),x)))
    st.session_state["actions"] = actions

init_sess_state("i",0)
init_sess_state( "feedbacks" , {})
init_sess_state ("campaign_id", 0)
init_sess_state( "nb_campaigns" , len(verbose))
init_sess_state( "motiv_done" , False)
init_sess_state("feedback_done",False)
init_sess_state( "finished" , False)
init_sess_state("motivations",[{} for _ in range(st.session_state["nb_campaigns"])])


#>>> Code of the page

st.title("Campagne d'opinion sur les actions participatives")
"Étape :", st.session_state.count+1,"sur 10" 

if st.session_state.count == 0:
    #Introduction page + personnal data form
    st.markdown(presentation)
    
    with st.form("Preliminary informations"):
        age = st.radio("Indiquez votre catégorie d'âge:",
        [   "entre 18 et 25 ans",
            "entre 26 et 40 ans",
            "entre 41 et 65 ans",
            "66 ans et plus",
            "Ne se prononce pas"])
        gender = st.radio("Précisez votre genre :",
        [   "Feminin",
            "Masculin",
            "Ne se prononce pas"])
        social_category = st.radio("Indiquez votre catégorie socio-professionnelle (échelle PCS2003):",
        [   "Agriculteurs/agricultrices exploitant.e.s",
            "Artisan.e.s, commerçant.e.s et chef.fe.s d'entreprise",
            "Cadres et professions intellectuelles supérieures",
            "Professions intermédiaires",
            "Employé.e.s",
            "Ouvrier.e.s",
            "Retraité.e.s",
            "Autres personnes sans activités professionnelles (dont militaires, étudiant.e.s)",
            "Ne se prononce pas"
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

    #Motivations collection
    if not st.session_state["motiv_done"] :
        motivations = {} 
        motiv_map = st.session_state["motiv_map"]
        
        # col1,col2 = st.columns(2)
        # with col1:
        #Hard-coded supplementary information collection
        st.image(f"imgs/im{c_id}.jpg")

        if c_id == 0:
            
            st.markdown("""## Expérimentation fictive numéro 1 : la tonte de gazon

D'abord: disons que vous ayez un jardin. """)
            habits = st.segmented_control(f"Si vous av(i)ez un jardin quelle est/serait votre fréquence de tonte habituelle ?",
                                        options=[
                                            "1 fois/semaine ou moins",
                                            "2 à 4 fois par mois",
                                            "1 fois par mois ou moins"
                                        ])
        st.markdown(verbose[st.session_state["campaign_id"]])


        with st.form("action_motivations"):
            for action in meaningful_actions[c_id]:
                motivation_string = st.segmented_control(
                    f"Voudriez-vous {meaningful_actions[c_id][action]} ?",
                    options=st.session_state["scale"], 
                    selection_mode="single")
                if motivation_string is not None:
                    motivations[action] = motiv_map[motivation_string]

            submitted = st.form_submit_button("Soumettre",type="primary",key=0)
            
            if submitted and len(motivations) == len(meaningful_actions[c_id])  and c_id ==0  and habits is not None:
                with st.spinner("Traitement de vos réponses en cours...", show_time=True):
                    add_motivations(c_id,st.session_state["n"],motivations,1,[habits])
                    st.session_state["motivations"][c_id] = motivations
                    st.session_state.count+=1
                    st.session_state["campaign_id"]= (c_id + 1)%st.session_state["nb_campaigns"]
                    st.session_state["motiv_done"] = (st.session_state["campaign_id"] == 0)
                    st.rerun()
            elif submitted and len(motivations) == len(meaningful_actions[c_id]) and c_id!=0:
                with st.spinner("Traitement de vos réponses en cours...", show_time=True):
                    add_motivations(c_id,st.session_state["n"],motivations)
                    st.session_state["motivations"][c_id] = motivations
                    st.session_state.count+=1
                    st.session_state["campaign_id"]= (c_id + 1)%st.session_state["nb_campaigns"]
                    st.session_state["motiv_done"] = (st.session_state["campaign_id"] == 0)
                    st.rerun()                
            elif submitted:
                "Completez toutes les questions du questionnaire s'il vous plaît."

    #Feedback collection
    if st.session_state["motiv_done"] and not st.session_state["feedback_done"]:
        st.image(f"imgs/im{c_id}.jpg")

        st.markdown(f"""## Votre avis sur :green[{campaign_names[c_id]}] """)
        st.markdown(verbose_feedback)
        with st.form("feedback"):
            print(st.session_state["i"])
            action = st.session_state["actions"][c_id][st.session_state["i"]]
            st.markdown(f"""
Les organisateurs de l'expérience vous demandent d'effectuer l'action suivante: :green[{meaningful_actions[c_id][action]}].
                    """)
            feedback = st.segmented_control(
                f"Pensez-vous que vous la réaliseriez du mieux possible ?",
                options=st.session_state["smaller_scale"], 
                selection_mode="single",
                key = st.session_state["i"]+10*st.session_state["campaign_id"])
            if feedback is not None:
                st.session_state["feedbacks"][action] = feedback
            submitted = st.form_submit_button("Soumettre",type="primary") 

            if submitted and feedback is not None and st.session_state["i"] == len(st.session_state["actions"][c_id])-1:
                with st.spinner("Traitement de vos réponses en cours...", show_time=True):
                    add_feedback(c_id,st.session_state["n"],st.session_state["motivations"][c_id], st.session_state["feedbacks"])
                    st.session_state.count+=1
                    st.session_state["i"] = 0
                    st.session_state["campaign_id"]= (c_id + 1)%st.session_state["nb_campaigns"]
                    st.session_state["feedback_done"] = (st.session_state["campaign_id"] == 0)
                    st.rerun()
            elif submitted and feedback is not None:
                st.session_state.count+=1
                st.session_state["i"]+=1
                st.cache_data.clear()
                st.rerun()
            elif submitted:
                "Completez toutes les questions du questionnaire s'il vous plaît."

    #Suggestion collection 
    if st.session_state["feedback_done"] and not st.session_state["finished"]: 
        with st.form("final_opinions"): 
            st.markdown("Merci pour vos réponses et votre participation à cette expérience.")
            suggestion = st.text_area("Vous pouvez fermer cet onglet ou nous donner vos suggestions ou votre avis sur cette campagne:",placeholder = "Écrire içi")
            submitted = st.form_submit_button("Soumettre")
            if submitted:
                add_suggestion(st.session_state["n"], suggestion)
                st.session_state["finished"] = True
                rerun()

    #Closing page
    if st.session_state["finished"]:
        "Merci d'avoir partagé votre avis et d'avoir participé à cette expérience ! Vous pouvez fermer cet onglet."



st.html("""<footer style="background-color:#f1f1f1; padding:20px;">
  <div style="display:flex; justify-content:center; gap:20px;">
    <img src="imgs/ANR_Logo.svg.png" alt="Image 1" style="width:80px; height:auto;">
    <img src="imgs/logo-irisa.png" alt="Image 2" style="width:80px; height:auto;">
    <img src="imgs/logo_iris-e.jpg" alt="Image 3" style="width:80px; height:auto;">
    <img src="imgs/ENS_LOGOcouleur_RVB.png" alt="Image 4" style="width:80px; height:auto;">
  </div>
</footer>""")
