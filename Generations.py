from planning_jour import *
from generation_jour import *
from Entree import *
import datetime as dt

##==========================================================================================
# CLASSE GÉNÉRATION
##==========================================================================================

class generation :

    def __init__(self, List_planning):
        self.List_planning = List_planning # List.planning et la liste des generation_jour...

    def Generation_init(self, nb_indiv):
        List_planning = []*nb_indiv
        List_planning.append(planning_jour)
        return List_planning

    def get_planning(self,id):
        return self.List_planning[id]

    #def test_chevauchement(self):

    def test_doublons(self):
        for i in range(len(self.List_planning)):
            for j in range(i,len(self.List_planning)):
                if self.List_planning[i]["Id"] == self.List_planning[j]["Id"]:
                    return True
        return False

    def affichage_generation_totale(self, jours):
        print("------------------------PLANNING TOTAL------------------------")
        print("Ensemble du planning sur la periode de voyage : ")
        for k in range(len(jours)):
            for timestamp in jours[k]:
                print(dt.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y"))

        for i in range(len(self.List_planning)):
            self.List_planning[i].affichage_generation_jour() 

##==========================================================================================
# generation du planning total 
##==========================================================================================

def generation_planning_total(jours, nb_planning_généré, dico_dicos, json_entree, nombre_diterations_choisi):
    planning_total = [] 
    for i in range (len(jours)):
        print("i-ème tranche de jour",i)
        #création du pool complet d'activité fille 
        pool_act_filles = creation_debut_act_fille(dico_dicos, jours[i], recup_plusHour(json_entree), recup_dinner(json_entree))
        if i == 0: # Si c'est la première paire de jours
            pool_activity = dico_activité_fille(dico_dicos, json_entree, pool_act_filles)# permet de créer un dico d'ojet activity rangé par id
            print("nb activité disponible dans le pool d'activité initial", len(pool_activity.keys()))
        else:       
            pool_activity = dico_activité_fille(dico_dicos, json_entree, pool_act_filles)
            pool_activity = modif_pool_activities(pool_activity, planning_total[-1].generation_journees[0].liste_id_dispo_suite)
        planning_total.append(generation_planning_unitaire(nb_planning_généré, pool_activity, jours[i], json_entree)) # génération de tous mes plannings possibles sur deux jours (48h) 
        print("nb activité disponible avant l'algorithme génétique",len(planning_total[-1].generation_journees[0].liste_id_dispo_suite))
        planning_total[-1].algo_genetique(nombre_diterations_choisi, pool_activity) # nombre_diterations_choisi à définir
        print("nb activité disponible après l'algorithme génétique",len(planning_total[-1].generation_journees[0].liste_id_dispo_suite))
    gene_tot = generation(planning_total)       
    return gene_tot

    
def modif_pool_activities(pool_activity, liste_id_restants):
    liste_id_pool_activity = pool_activity
    new_pool_activity = {}
    for act_id in liste_id_restants:
        new_pool_activity[act_id] = pool_activity[act_id]
    return new_pool_activity
