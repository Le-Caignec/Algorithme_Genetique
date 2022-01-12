from recupActivitiesMother import *
from Entree import *
from activity import *
from Creation_activités_filles import *
from activity import *
from enfant_planning import *
from Generations import *
from GUI_calandar import *
from time import *
from generation_jour import *
from planning_jour import *
from Sortie import *
import flask
from flask import request, jsonify
##==========================================================================================
# MAIN DE L'ALGORITHME GÉNÉTIQUE
##==========================================================================================

#exemple requète GET
#http://0.0.0.0:500/api_algorithme_genetique?nb_planning_initial=4&nb_iteration_choisi=10&json_entree={"data":{"area":"48.8326935,2.3591803","select":["76687504-33eb-11eb-9b45-0cc47a0803e4","7910b0bb-33d1-11eb-9b45-0cc47a0803e4","07cab010-026e-11eb-9cde-0cc47a0803e4","4eee423e-751c-11eb-b183-0cc47a0803e4","fb62c00f-0304-11eb-9cde-0cc47a0803e4","af42490c-7513-11eb-b183-0cc47a0803e4","a683564b-5139-11e8-8390-02420a000106","44142fb1-040a-11eb-9cde-0cc47a0803e4","9b233677-7514-11eb-b183-0cc47a0803e4","95b56ad0-751a-11eb-b183-0cc47a0803e4","119976a1-7518-11eb-b183-0cc47a0803e4","d0d3b6b5-7515-11eb-b183-0cc47a0803e4","6ba319bd-0318-11eb-9cde-0cc47a0803e4","cf29165d-750a-11eb-b183-0cc47a0803e4","3cb3e629-7506-11eb-b183-0cc47a0803e4","4dde0ddd-1aeb-11eb-918b-0cc47a0803e4","d8a721e5-7506-11eb-b183-0cc47a0803e4","36f1b893-7517-11eb-b183-0cc47a0803e4","0f33dac5-50a4-11e8-8390-02420a000106","1576b129-0308-11eb-9cde-0cc47a0803e4","886a9946-b1fb-11e9-9c81-0cc47a0803e4","1c139080-750b-11eb-b183-0cc47a0803e4"],"search":"start=1%26data%5Bpays%5D=France%26data%5Bville%5D=Paris%26data%5Bdates%5D=25%2F06%2F2021+-+31%2F06%2F2021%26passengers=2%26new0=on%26data%5Binput%5D%5B0%5D=14%2F04%2F1980%26new1=on%26data%5Binput%5D%5B1%5D=21%2F11%2F2014"},"mode":"transit","dinner":"1","plushour":"32400","session_csrf":"3gvfhr3b4d8gk"}

app = flask.Flask(__name__)
@app.route('/api_algorithme_genetique', methods=['GET'])

def GET():
    # nb_planning_généré = 1
    # while (not nb_planning_généré%4 == 0):
    #     print("Veuillez rentrez un entier divisible par 4")
    #     nb_planning_généré = int(input("Choisir le nombre de planning : "))

    # nombre_diterations_choisi = int(input("Choisir le nombre d'iteration choisi pour l'algorithme génétique : "))
    nb_planning_généré=request.args.get("nb_planning_initial")
    nombre_diterations_choisi=request.args.get("nb_iteration_choisi")
    if (nb_planning_généré%4 == 0):
        #Json d'entrée = informations rentrées par l'utilisateur sur le site
        json_entree=request.args.get("json_entree")

        #On démarre le chronométre pour déterminer le temps d'éxécution du programme par le CPU
        tps1 = perf_counter()
        
        #Récupération des ID des activités depuis le json utilisateur
        list_id = list(set(recup_ids(json_entree))) # permet d'éviter les doublons dans la liste d'id 

        #Connexion à la base donnée pour créer les activités mère de l'algorithme
        conn = connect()
        dico_dicos = get_activity_by_id(conn, list_id)

        #Création du pool des horaires possibles d'act filles
        jours = decoupage_sejour(recup_search(json_entree)["dates"])

        gene_tot = generation_planning_total(jours, nb_planning_généré, dico_dicos, json_entree, nombre_diterations_choisi)
        
        #affichage consol du planning finale 
        #gene_tot.affichage_generation_totale(jours)
        
        #création d'un json de sortie de l'API
        json_sortie = retour_API(gene_tot, dico_dicos, json_entree)

        #affichage du temps d'éxécution du programme par le CPU sans l'affichage dans l'API calandar
        tps2 = perf_counter() 
        print("TEMPS EXECUTION CPU SANS l'AFFICHAGE : ",tps2 - tps1)
        
        #affcihage du meilleur planning construit par l'algorithme génétique 
        affichage_algo_genetique(gene_tot, json_entree)

    
        #affichage du temps d'éxécution du programme par le CPU avec l'affichage de l'API calanadar
        tps3 = perf_counter()
        print("TEMPS EXECUTION CPU AVEC l'AFFICHAGE : ",tps3 - tps1)

        # j'affiche la sortie de l'API
        return json_sortie
    else:
        return jsonify("Veuillez rentrez un nombre de planning initial divisible par 4")

#je fait tourner le code en serveur locale accesible à l'adresse ip: 0.0.0.0 et au port:500
app.run(debug=True, host='0.0.0.0', port=500)
