from planning_jour import *
from enfant_planning import *
import datetime as dt
import copy as copy
import random

##==========================================================================================
# CLASSE GÉNÉRATION_JOUR
##==========================================================================================

class generation_jour :

    def __init__(self, generation_journees, pool_id_dispos):# pool_id_dispos=list(pool_activity.keys())
        self.generation_journees = generation_journees
        self.pool_id_dispos = pool_id_dispos # Listes des activites restantes dispo pour les prochaines périodes de 2 jours de planning

    def affichage_generation_jour(self):
        print("------------------------GÉNÉRATION JOUR------------------------")
        print("Plannings générés sur deux journées :")
        for planning in self.generation_journees:
            print([datetime.fromtimestamp(jour) for jour in planning.jour])
            planning.affichage_planning_jour()
            print("\n")
            print("\n")
            print("\n")

    ##==========================================================================================
    # TOURNOI
    ##==========================================================================================

    def tournoi_best_half(self):
        generation_post_tournoi = sorted(self.generation_journees, key=lambda planning_jour: planning_jour.note, reverse=True)
        del generation_post_tournoi[int(len(generation_post_tournoi)/2):] #On garde la premiere moitié de la generation 
        self.generation_journees = generation_post_tournoi

        # for i in range(len(generation_post_tournoi)):
        #     print("note n° ", i+1, " : ", generation_post_tournoi[i].note)

    ##==========================================================================================
    # REPRODUCTION
    ##==========================================================================================

    def parcours(self, liste_activite_1, liste_activite_2):
        liste_pause_commune = [] 
        for i in range(len(liste_activite_1)-1): #On compare une activité de i avec toutes celle du planing 2
            for j in range(len(liste_activite_2)-1):  
                
                activite_terminant_le_plus_tard = 0                  
                if(liste_activite_1[i][1]>=liste_activite_2[j][1]): #On test si l'activité i considérée se termine plus tard que l'activité j
                    activite_terminant_le_plus_tard = liste_activite_1[i][1] #Si cest le cas elle devient l'activité se terminant le plus tard
                else: 
                    activite_terminant_le_plus_tard = liste_activite_2[j][1] #Sinon cest l'autre
                
                activite_commencant_le_plus_tot = 0          
                if(liste_activite_1[i+1][0]<=liste_activite_2[j+1][0]): 
                    activite_commencant_le_plus_tot = liste_activite_1[i+1][0]
                else: 
                    activite_commencant_le_plus_tot = liste_activite_2[j+1][0]
                
                if(activite_terminant_le_plus_tard<activite_commencant_le_plus_tot):
                    liste_pause_commune.append([activite_terminant_le_plus_tard,activite_commencant_le_plus_tot]) #On append les temps de pause commune   
        return liste_pause_commune

    def detection_pause_commune_pour_crossover(self, planning_1_entree, planning_2_entree, nb_jour):
        jour = planning_1_entree.jour
        pause_dejeuner = planning_1_entree.pause_dejeuner
        lieu_depart = planning_1_entree.lieu_depart
        heure_debut_journee = planning_1_entree.heure_debut_journee
        mode_transport = planning_1_entree.mode_transport

        planning_1 = planning_1_entree.liste_enfant_planning #liste d'enfants planning
        planning_2 = planning_2_entree.liste_enfant_planning
        # crossover simple par le bas
        # On va regarder un indice a partir duquel on peut faire le crossover puis le realiser
        nb_jour_en_minute = 1440*nb_jour
        liste_activite_1 = []
        liste_activite_2 = []
        liste_activite_1.append([0,0])
        liste_activite_2.append([0,0])
        
        for i in range(len(planning_1)): #Par construction les listes de planning sont déja triées
            fin_activite = planning_1[i].debut_activity + planning_1[i].nombre_unites
            liste_activite_1.append([planning_1[i].debut_activity, fin_activite]) # tableau 2D avec le debut et la fin
        
        for i in range(len(planning_2)):
            fin_activite = planning_2[i].debut_activity + planning_2[i].nombre_unites
            liste_activite_2.append([planning_2[i].debut_activity, fin_activite]) #On garde toutes les activités dont la fin se place apres l'indice
            
        liste_activite_1.append([nb_jour_en_minute, nb_jour_en_minute])
        liste_activite_2.append([nb_jour_en_minute, nb_jour_en_minute])
        
        liste_pause_commune = self.parcours(liste_activite_2,liste_activite_1) #On enleve les pauses du debut du jour 1 et la pause du dernier jours 
        #Sans quoi on pourrait obtenir des enfants clones
        
        liste_pause_commune.pop(-1)

        indice_random_liste = 0

        if (len(liste_pause_commune) > 1):
            liste_pause_commune.pop(0)
            indice_random_liste = random.randint(0, len(liste_pause_commune) - 1) 

        timestamp_random = 0

        if (len(liste_pause_commune) > 1):
            timestamp_random = int((liste_pause_commune[indice_random_liste][0] + liste_pause_commune[indice_random_liste][1])/2) 
        
        debut_enfant_1 = []
        debut_enfant_2 = []     

        fin_enfant_1 = []
        fin_enfant_2 = []     

        liste_id_1 = [] # Liste des id des activités des enfants 1 et 2
        liste_id_2 = []

        indice_1 = 0
        indice_2 = 0
        #On forme les enfants en faisant attention de ne pas avoir des ID clones

        for i in range(len(planning_1)): 
            if(planning_1[i].debut_activity < timestamp_random):
                indice_1 = i
                if(planning_1[i].activity.Id not in liste_id_1):
                    debut_enfant_1.append(planning_1[i]) #Ajoute des enfants plannings dans une liste initialement vide
                    liste_id_1.append(planning_1[i].activity.Id)

            elif planning_1[i].activity.Id not in liste_id_2:
                fin_enfant_2.append(planning_1[i])
                liste_id_2.append(planning_1[i].activity.Id)

        for i in range(len(planning_2)):
            if(planning_2[i].debut_activity < timestamp_random):
                indice_2 = i
                if planning_2[i].activity.Id not in liste_id_2 : 
                    debut_enfant_2.append(planning_2[i])
                    liste_id_2.append(planning_2[i].activity.Id)

            elif planning_2[i].activity.Id not in liste_id_1:
                fin_enfant_1.append(planning_2[i])
                liste_id_1.append(planning_2[i].activity.Id)

        enfant_1 = self.coherence_temps_parcours_activite(debut_enfant_1,fin_enfant_1,mode_transport)
        enfant_2 = self.coherence_temps_parcours_activite(debut_enfant_2,fin_enfant_2,mode_transport)

        #A FAIRE : REMETTRE A JOUR LES TEMPS DE TRAJETS ENTRE DEUX ACTIVITES BRO

        liste_id_suite_enfant_1 = copy.deepcopy(self.pool_id_dispos)
        liste_id_suite_enfant_2 = copy.deepcopy(self.pool_id_dispos)

        for act_id in liste_id_1:
            liste_id_suite_enfant_1.remove(act_id)

        for act_id in liste_id_2:
            liste_id_suite_enfant_2.remove(act_id)

        gen_1 = planning_jour(enfant_1, jour, pause_dejeuner, lieu_depart, heure_debut_journee, liste_id_suite_enfant_1, mode_transport)
        gen_2 = planning_jour(enfant_2, jour, pause_dejeuner, lieu_depart, heure_debut_journee, liste_id_suite_enfant_2, mode_transport)
        gen_1.fonction_evaluation()
        gen_2.fonction_evaluation()

        return (gen_1, gen_2) #On envoie deux plannings sans verifier le probleme des temps de trajet. 

        
    def coherence_temps_parcours_activite(self, debut_enfant, fin_enfant, mode_transport):
        if len(debut_enfant)>0:
            if(len(debut_enfant)>0 and len(fin_enfant)>0):
                while(len(fin_enfant) > 0): 
                    temps_trajet = 0
                    if(len(debut_enfant[-1].activity.localisation)==2 and len(fin_enfant[0].activity.localisation)==2):   
                        temp1 = debut_enfant[-1].activity.localisation[0]
                        temp2 = debut_enfant[-1].activity.localisation[1]
                        temp3 = fin_enfant[0].activity.localisation[0]
                        temp4 = fin_enfant[0].activity.localisation[1]

                        temps_trajet = temps_de_trajet_deux_activites(temp1, temp2, temp3, temp4, mode_transport)

                        if(debut_enfant[-1].debut_activity + debut_enfant[-1].nombre_unites + temps_trajet > fin_enfant[0].debut_activity):
                            fin_enfant.pop(0)
                        else:
                            fin_enfant[0].temps_act_precedente = temps_trajet
                            break 
        return debut_enfant + fin_enfant
        
    def crossover(self):
        liste_indices = [i for i in range (len(self.generation_journees))]
        random.shuffle(liste_indices)
        new_generation = self.generation_journees
        for i in range (0, len(self.generation_journees), 2):
            indices_aleat_1 = liste_indices[i]
            indices_aleat_2 = liste_indices[i+1]
            nb_jour = len(self.generation_journees[indices_aleat_1].jour)
            enfant1, enfant2 = self.detection_pause_commune_pour_crossover(self.generation_journees[indices_aleat_1], self.generation_journees[indices_aleat_2], nb_jour)
            new_generation.append(enfant1)
            new_generation.append(enfant2)
        self.generation_journees = new_generation


    ##==========================================================================================
    # ALGORITHME GÉNÉTIQUE
    ##==========================================================================================
    def algo_genetique(self, nombre_diterations_choisi, pool_activity):
        liste_note_meilleur = []
        for i in range (nombre_diterations_choisi):
            # Tournoi
            self.tournoi_best_half() 
            liste_note_meilleur.append(self.generation_journees[0].note)

            # Cross over
            self.crossover()
            
            for i in range (len(self.generation_journees)):
                id_enfant_planing_choisi = [id for id in self.generation_journees[i].liste_id_dispo_suite]
                n = random.random()
                if (n <= 0.01):
                        # Mutations par deletion
                        self.generation_journees[i].mutation_deletion()

                for id_restant in id_enfant_planing_choisi:
                    choice = random.random()
                    # Voir pour savoir quelle mutation mettre en premier
                    
                    
                    if(choice <= 0.5):
                        #on choisit un enfant planning parmi la liste des id des enfants disponibles
                        acti = pool_activity[id_restant]
                
                        # Mutations par insertion
                        rajout_act = self.generation_journees[i].mutation_par_insertion(acti)
                        if rajout_act:
                            self.generation_journees[i].liste_id_dispo_suite.remove(id_restant)

        print ("Evolution des meilleurs plannings : ", liste_note_meilleur)

##==========================================================================================
# Calcul du premier début possible pour la prochaine activity que l'on souhaite placer
##==========================================================================================

def calcul_debut_activity(pool_activity, id_choisi, liste_enfant_planning, indice_jour, json_entree):
    #cas de base si la liste_enfant_planning est vide, on retourne le premier horaire disponible
    debut_activity = None
    temps_de_trajet = 0
    if (len(liste_enfant_planning) == 0):
        temps_de_trajet = float(temps_de_trajet_deux_activites(recup_area(json_entree)["latitude"], recup_area(json_entree)["longitude"], pool_activity[id_choisi].localisation[0], pool_activity[id_choisi].localisation[1], recup_mode(json_entree)))
        if (pool_activity[id_choisi].visite_libre):
            heure_possible = pool_activity[id_choisi].list_begin_hours[indice_jour]
            for liste in heure_possible:  
                for k in range (liste[0], liste[1], 60): # K est l'heure de début, minute par minute
                    if ((k + int(pool_activity[id_choisi].duration) <= int(liste[1])) and (k >= (recup_plusHour(json_entree) + float(temps_de_trajet)))):
                        debut_activity = k 
                        return debut_activity, temps_de_trajet
        elif (not pool_activity[id_choisi].visite_libre):
            heure_possible = pool_activity[id_choisi].list_begin_hours[indice_jour]
            for heure in heure_possible:
                if (int(heure) >= (recup_plusHour(json_entree) + float(temps_de_trajet))):
                    debut_activity = int(heure) 
                    return debut_activity, temps_de_trajet

    else: 
        temps_de_trajet = float(temps_de_trajet_deux_activites(liste_enfant_planning[-1].activity.localisation[0], liste_enfant_planning[-1].activity.localisation[1], pool_activity[id_choisi].localisation[0], pool_activity[id_choisi].localisation[1], recup_mode(json_entree)))
        if (pool_activity[id_choisi].visite_libre):
            heure_possible = pool_activity[id_choisi].list_begin_hours[indice_jour]
            for liste in heure_possible:
                for k in range (liste[0], liste[1], 60):
                    if ((k + int(pool_activity[id_choisi].duration)) <= int(liste[1])) and (k >= (int(liste_enfant_planning[-1].debut_activity)*60 + int(liste_enfant_planning[-1].activity.duration) + float(temps_de_trajet))):
                        debut_activity = k 
                        return debut_activity, temps_de_trajet
        else: 
            heure_possible = pool_activity[id_choisi].list_begin_hours[indice_jour]
            for heure in heure_possible:
                if (int(heure) >= (int(liste_enfant_planning[-1].debut_activity)*60 + int(liste_enfant_planning[-1].activity.duration) + float(temps_de_trajet))):
                    debut_activity = int(heure) 
                    return debut_activity, temps_de_trajet
    return debut_activity, temps_de_trajet
    
##==========================================================================================
# Retourne la liste des ID des activity qui sont disponibles le Jour 1
##==========================================================================================
def ids_dispo_J1(pool_activity, periode):
    list_ids_dispo_J1 = []
    for keys, valeur in pool_activity.items():
        if (int(pool_activity[keys].liste_de_jours[0]) == int(periode[0])):
            list_ids_dispo_J1.append(keys)
    return list_ids_dispo_J1

##==========================================================================================
# Retourne la liste des ID des activity qui sont disponible le Jour 2 mais qui n'ont pas été utilisées pour le jour 1
##==========================================================================================
def ids_dispo_J2(pool_activity, liste_enfant_planning, periode):
    list_ids_dispo_J2 = []
    if (len(periode) == 2):
        for keys, valeur in pool_activity.items():
            if (int(pool_activity[keys].liste_de_jours[1]) == int(periode[1])):
                list_ids_dispo_J2.append(keys)
        for planning_enfant in liste_enfant_planning:
                if (planning_enfant.activity.Id in list_ids_dispo_J2):
                    list_ids_dispo_J2.remove(planning_enfant.activity.Id)
    return list_ids_dispo_J2

##==========================================================================================
# Génération des plannings sur deux jours
##==========================================================================================

def generation_planning_unitaire(nb_planning_générés, pool_activity, periode, json_entree): # génération de tous mes plannings possibles sur deux jours (48h)
    liste_generation_planning = [] #Ensemble des plannings sur 2 jours
    for k in range (int(nb_planning_générés)): # Boucle pour définir un nombre fixé de plannings
        List_dispo_jour = [] #Liste des listes des ids dispo pour les différents jours
        liste_enfant_planning = [] #Ensemble des enfant_planning que l'on va placer
        temps_enfant_planning = [] #Liste temporaire remplie d'enfants et remise à zéro à la fin du jour
        list_ids_dispo_1 = ids_dispo_J1(pool_activity, periode) #list des id disponibles pour le jour 1
        List_dispo_jour.append(list_ids_dispo_1)
        for i in range (len(periode)): # on effectue les opérations suivant le fait qu'il y ait un ou deux jours
            random.shuffle(List_dispo_jour[i]) # mélange la liste des ids
            indice_list = 0 # à incrémenter si on ne supprime pas l'id de la liste 
            while (indice_list < (len(List_dispo_jour[i])) and (len(List_dispo_jour[i]) != 0)):
                debut_activity, temps_de_trajet = calcul_debut_activity(pool_activity, List_dispo_jour[i][indice_list], temps_enfant_planning, i, json_entree)
                if ((len(temps_enfant_planning) == 0) and (debut_activity is not None)):
                    planning_enfant = enfant_planning(debut_activity, pool_activity[List_dispo_jour[i][indice_list]],temps_de_trajet, periode[i])
                    temps_enfant_planning.append(planning_enfant) 
                    List_dispo_jour[i].remove(List_dispo_jour[i][indice_list])
                # il y a déjà un planning enfant placé. pour en ajouter un autre il faut vérifier les condition suivantes:
                # - temps de trajet avec l'activité précédente est possible
                # - l'activité possède un créneau après l'activité déjà placée 
                # - l'activité possiblement placée ne déborde ps obligatoirement sur la fin de journée ou la pause déjeunée
                else :
                    if (debut_activity is None) :
                        indice_list += 1
                    else:
                        planning_enfant = enfant_planning(debut_activity, pool_activity[List_dispo_jour[i][indice_list]],temps_de_trajet, periode[i])
                        temps_enfant_planning.append(planning_enfant) 
                        List_dispo_jour[i].remove(List_dispo_jour[i][indice_list])
            list_ids_dispo_2 = ids_dispo_J2(pool_activity,temps_enfant_planning,periode) #on forme une liste avec les IDs disponibles le jour 2 et qui n'ont pas encore été pris
            List_dispo_jour.append(list_ids_dispo_2)
            liste_enfant_planning.append(temps_enfant_planning)
            temps_enfant_planning = []
        jour = periode
        pause_dejeuner = recup_dinner(json_entree)
        lieu_depart = recup_area(json_entree)
        heure_debut_journee = recup_plusHour(json_entree) 
        liste_finale = liste_enfant_planning[0]
        if (len(periode) == 2):
            for i in range (len(liste_enfant_planning[1])):
                liste_enfant_planning[1][i].debut_activity += 1440.0
                liste_finale.append(liste_enfant_planning[1][i])
        liste_id_restants = list(pool_activity.keys())
        liste_id_utilises = [element.activity.Id for element in liste_finale]
        for act_id in liste_id_utilises:
             liste_id_restants.remove(act_id)
        liste_generation_planning.append(planning_jour(liste_finale, jour, pause_dejeuner, lieu_depart, heure_debut_journee, liste_id_restants, recup_mode(json_entree)))
            
    generation_journees = generation_jour(liste_generation_planning, list(pool_activity.keys()))
    return generation_journees

