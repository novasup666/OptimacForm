
meaningful_actions = [
            {"weekly":"tondre votre gazon une fois par semaine",
            "monthly":"tondre votre gazon une fois par mois",
            "as_usual":"tondre comme d'habitude"},
            {"weekly":"placer des graines une fois par semaine",
            "monthly":"placer des graines une fois par mois",
            "notatall":"ne pas placer de graines"}]

presentation = """
Le projet OptimAc est mené par l'équipe DRUID de l'IRISA. Son objectif est de fournir des outils pour la mise en place de campagnes d'action participatives. 

Ces campagnes ont la particularité de faire participer les citoyens à la production de données scientifiques au travers de la réalisation concrète d'expériences. Par exemple: tondre son gazon à une certaine fréquence (ex. 1 fois/semaine) et tenir compte de l'évolution de la biodiversité dans ledit jardin.

L'une des tâches du projet OptimAc est de modéliser le comportement de participants à de telles campagnes pour pouvoir affiner la méthode avec laquelle attribuer ces expériences aux participants.

Ainsi, vous allez participer à deux campagnes fictives qui seront détaillées plus loin. 

Pas d'inquiétudes ! Vous n'avez besoin que de cinq minutes pour remplir ce formulaire (et même pas besoin de jardin !).


Avant de commencer, petit point données personnelles: 
- Nous avons besoin de collecter quelques informations personnelles à des fins statistiques. 
- Nous vous informons que nous ne collectons que les données que vous fournirez dans ce formulaire.
- Toute réponse soumise à ce formulaire est hébergée par Google et donc potentiellement en dehors de l'Union européenne. 
- La soumission du formulaire suivant vaut pour acceptation du stockage de ces données sur les serveurs de GOOGLE et de leur exploitation pleine et entière par les membres présents et futurs de l'équipe DRUID de l'IRISA. 
    """


verbose = [
    """
## Expérimentation fictive numéro 1 : la tonte de gazon


D'abord: disons que vous ayez un jardin. 

Votre tâche serait la suivante :
- Tondre votre gazon à la fréquence demandée.
- Effectuer un inventaire des insectes sur une surface donnée une fois toutes les deux semaines.


Quelle fréquence de tonte seriez-vous d'accord d'adopter le temps d'une expérience d'un mois ?

Vous allez devoir juger les différentes propositions, nous vous demandons de le faire le plus honnêtement possible, en essayant de vous projeter. N'hésitez pas à prendre votre temps!


""",
"""
## Expérimentation fictive numéro 2 : le nourrissage d'oiseaux


Votre tâche serait la suivante:
- Placer une certaine quantité de graines pour oiseaux sur un rebord de fenêtre, votre balcon ou votre terrasse, selon la fréquence demandée.
- Effectuer un décompte du nombre d'oiseaux aperçus autour de votre logement, une fois par semaine pendant une vingtaine de minutes.

À quelle fréquence voudriez-vous placer des graines sur votre rebord de fenêtre ou balcon ?

Vous allez devoir juger les différentes propositions, nous vous demandons de le faire le plus honnêtement possible, en essayant de vous projeter. N'hésitez pas à prendre votre temps!
"""
]

verbose_feedback="""
Dans cette phase de l'expérience, vous vous voyez attribuer une action et nous vous demanderons d'indiquer si vous pensez que vous mettriez vraiment cette action en place ou si vous pensez que vous n'arriveriez pas à vous y tenir. 
De la même façon, soyez le plus honnête et n'hésitez pas à prendre votre temps.
"""

campaign_names = ["la tonte du gazon", "le nourrissage des oiseaux"]