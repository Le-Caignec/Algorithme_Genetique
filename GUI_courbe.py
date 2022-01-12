import numpy as np
import matplotlib.pyplot as plt
from Generations import *
# %matplotlib inline

##==========================================================================================
# 1ere Courbe : Evolution des notes du meilleur planning en fonction du nombre d'itération
##==========================================================================================

def courbe_note_iteration(nombre_diterations_choisi,pop_depart):
    list_nb_iteration=[ k for k in range (0,nombre_diterations_choisi,1)]
    list_note_total=[]
    #Json d'entrée = informations rentrées par l'utilisateur sur le site
    json_entree={"data":{"area":"48.8326935,2.3591803","select":["76687504-33eb-11eb-9b45-0cc47a0803e4","7910b0bb-33d1-11eb-9b45-0cc47a0803e4","07cab010-026e-11eb-9cde-0cc47a0803e4","4eee423e-751c-11eb-b183-0cc47a0803e4","fb62c00f-0304-11eb-9cde-0cc47a0803e4","af42490c-7513-11eb-b183-0cc47a0803e4","a683564b-5139-11e8-8390-02420a000106","44142fb1-040a-11eb-9cde-0cc47a0803e4","9b233677-7514-11eb-b183-0cc47a0803e4","95b56ad0-751a-11eb-b183-0cc47a0803e4","119976a1-7518-11eb-b183-0cc47a0803e4","d0d3b6b5-7515-11eb-b183-0cc47a0803e4","6ba319bd-0318-11eb-9cde-0cc47a0803e4","cf29165d-750a-11eb-b183-0cc47a0803e4","3cb3e629-7506-11eb-b183-0cc47a0803e4","4dde0ddd-1aeb-11eb-918b-0cc47a0803e4","d8a721e5-7506-11eb-b183-0cc47a0803e4","36f1b893-7517-11eb-b183-0cc47a0803e4","0f33dac5-50a4-11e8-8390-02420a000106","1576b129-0308-11eb-9cde-0cc47a0803e4","886a9946-b1fb-11e9-9c81-0cc47a0803e4","1c139080-750b-11eb-b183-0cc47a0803e4"],"search":"start=1&data%5Bpays%5D=France&data%5Bville%5D=Paris&data%5Bdates%5D=25%2F06%2F2021+-+28%2F06%2F2021&passengers=2&new0=on&data%5Binput%5D%5B0%5D=14%2F04%2F1980&new1=on&data%5Binput%5D%5B1%5D=21%2F11%2F2014"},"mode":"transit","dinner":"1","plushour":"32400","session_csrf":"3gvfhr3b4d8gk"}
    #Récupération des ID des activités depuis le json utilisateur
    list_id = list(set(recup_ids(json_entree))) # permet d'éviter les doublons dans la liste d'id 
    #Connexion à la base donnée pour créer les activités mère de l'algorithme
    conn = connect()
    dico_dicos = get_activity_by_id(conn, list_id)
    #Création du pool des horaires possibles d'act filles
    jours = decoupage_sejour(recup_search(json_entree)["dates"])

    for iteration in list_nb_iteration:
        list_note = []
        gene_tot = generation_planning_total(jours, pop_depart, dico_dicos, json_entree, iteration)
        for generation_dune_periode in gene_tot.List_planning:
            note = generation_dune_periode.generation_journees[0].note
            list_note.append(note)
        list_note_total.append(list_note)

    print("list_note_total",list_note_total)
    print("list_nb_iteration",list_nb_iteration)

    for k in range(len(list_note_total[0])):
        plt.plot(list_nb_iteration, [list_note_total[i][k] for i in range(len(list_note_total))], label = "Créneau de jour : "+ str(k))
    plt.legend()
    plt.title('Evolution des notes du meilleur planning en fonction du nombre d itération')
    plt.show()

##==========================================================================================
# 2 eme Courbe : Evolution des notes du meilleur planning en fonction de la population de départ
##==========================================================================================

def histogramme_note_population(nombre_diterations_choisi, pop_depart, nb_dhistogramme):
    json_entree = {"data":{"area":"48.8326935,2.3591803","select":["76687504-33eb-11eb-9b45-0cc47a0803e4","7910b0bb-33d1-11eb-9b45-0cc47a0803e4","07cab010-026e-11eb-9cde-0cc47a0803e4","4eee423e-751c-11eb-b183-0cc47a0803e4","fb62c00f-0304-11eb-9cde-0cc47a0803e4","af42490c-7513-11eb-b183-0cc47a0803e4","a683564b-5139-11e8-8390-02420a000106","44142fb1-040a-11eb-9cde-0cc47a0803e4","9b233677-7514-11eb-b183-0cc47a0803e4","95b56ad0-751a-11eb-b183-0cc47a0803e4","119976a1-7518-11eb-b183-0cc47a0803e4","d0d3b6b5-7515-11eb-b183-0cc47a0803e4","6ba319bd-0318-11eb-9cde-0cc47a0803e4","cf29165d-750a-11eb-b183-0cc47a0803e4","3cb3e629-7506-11eb-b183-0cc47a0803e4","4dde0ddd-1aeb-11eb-918b-0cc47a0803e4","d8a721e5-7506-11eb-b183-0cc47a0803e4","36f1b893-7517-11eb-b183-0cc47a0803e4","0f33dac5-50a4-11e8-8390-02420a000106","1576b129-0308-11eb-9cde-0cc47a0803e4","886a9946-b1fb-11e9-9c81-0cc47a0803e4","1c139080-750b-11eb-b183-0cc47a0803e4"],"search":"start=1&data%5Bpays%5D=France&data%5Bville%5D=Paris&data%5Bdates%5D=25%2F06%2F2021+-+28%2F06%2F2021&passengers=2&new0=on&data%5Binput%5D%5B0%5D=14%2F04%2F1980&new1=on&data%5Binput%5D%5B1%5D=21%2F11%2F2014"},"mode":"transit","dinner":"1","plushour":"32400","session_csrf":"3gvfhr3b4d8gk"}
    #Récupération des ID des activités depuis le json utilisateur
    list_id = list(set(recup_ids(json_entree))) # permet d'éviter les doublons dans la liste d'id 
    #Connexion à la base donnée pour créer les activités mère de l'algorithme
    conn = connect()
    dico_dicos = get_activity_by_id(conn, list_id)
    #Création du pool des horaires possibles d'act filles
    jours = decoupage_sejour(recup_search(json_entree)["dates"])

    for iteration in list_nb_iteration:
        list_note = []
        gene_tot = generation_planning_total(jours, pop_depart, dico_dicos, json_entree, iteration)

    for i in range(0, len(gene_tot.List_planning), len(gene_tot.List_planning)//5): # on doit demander un nombre divisible par 10 et donc 5 ? voir d'autres options
        liste_notes = [planning.note for planning in gene_tot.List_planning[-1].generation_journees]
        plt.figure(figsize=(12,10))
        plt.hist(liste_notes, align="mid", rwidth=0.9, color="b", edgecolor="blue", label="Nombre d'individus par groupe de note")
        plt.title("Histogramme présentant le nombre d'individus par groupement de notes")
        plt.xlabel("Note (fonction d'évaluation")
        plt.ylabel("Fréquence")
        plt.legend()
        plt.show()


print(courbe_note_iteration(20,20))

