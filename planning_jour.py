## IMPORTS
from activity import *
from math import *
from enfant_planning import *
from Entree import *
import datetime as dt
import random

##==========================================================================================
# CLASSE PLANNING D'UN JOUR
##==========================================================================================

class planning_jour:

    def __init__(self,liste_enfant_planning, jour, pause_dejeuner, lieu_depart, heure_debut_journee, liste_id_dispo_suite , mode_transport  ): #pause_dejeuner = recup_dinner(json_entree), lieu_depart = recup_area(json_entree), heure_debut_journee = recup_plushour(json_entree)
        self.liste_enfant_planning = liste_enfant_planning # Liste d'objet d'enfant_planning
        self.jour = jour # La liste des 2 jours correspondant au planning, en timestamp
        self.pause_dejeuner = pause_dejeuner # booleen precisant si on veut une pause dejeuner
        self.lieu_depart = lieu_depart 
        self.heure_debut_journee = heure_debut_journee
        self.note = self.fonction_evaluation()
        self.liste_id_dispo_suite = liste_id_dispo_suite # Id qui peuvent etre utilisé pour ajouter des activités apres : qu'est ce qu'on peut ajouter au planning, utilisé pour les jours suivant
        self.mode_transport = mode_transport
  
    def affichage_planning_jour(self):
        print("------------------------PLANNING------------------------")
        print("Jour du planning : ", self.jour)
        print("Lieu de départ : ", self.lieu_depart)
        print("Si l'utilisateur souhaite ou non une pause déjeuner : ",self.pause_dejeuner)
        print("Note d'évalutation : ", self.note)
        print("Planning de la journée : ")
        if len(self.liste_enfant_planning) == 0:
            print("Pas d'activités")
        else:
            for k in range (len(self.liste_enfant_planning)):
                self.liste_enfant_planning[k].affichage_enfant_planning()
    
    ##==========================================================================================
    # Evalutaion
    ##==========================================================================================

    def fonction_evaluation(self):
        # dans l'ordre de valorisation des utilités : nombre (^2), marge (*10), prix (*1), temps d'attente (*2 sur 60) et temps de trajet (*1 sur 60)
        planing_activite_deux_jours = self.liste_enfant_planning

        utilite_nb_act = 3*int(pow(len(planing_activite_deux_jours),6)) #On la met en int pour de la lisibilité, en ^2 pour valoriser le nombre d'activités
        utilite_temps_trajet = 0
        utilite_temp_attente = 0
        utilite_cout = 0
        utilite_marge = 0
        indice_jour = 0
        utilite_jour_vide = 0
        if(len(planing_activite_deux_jours)<len(self.jour)):
            utilite_jour_vide = -100000000000000

        for i in range(len(planing_activite_deux_jours) - 1): #calcul temps de trajet et temps d'attente                    

            jour_timestamp = planing_activite_deux_jours[i].jour

            debut_act_suivante = planing_activite_deux_jours[i+1].debut_activity # debut suivant
            fin_act_actuelle = planing_activite_deux_jours[i].debut_activity + planing_activite_deux_jours[i].nombre_unites # fin actuelle
            temps_trajet = planing_activite_deux_jours[i].temps_act_precedente * 500 # temps entre deux

            utilite_temps_trajet += temps_trajet
            
            utilite_cout += (planing_activite_deux_jours[i].activity.Price[jour_timestamp])*20 #On penalise le cout (prix) de l'activité (*1)
            utilite_marge += (planing_activite_deux_jours[i].activity.margin[jour_timestamp])*10 #valorisation en *10 de la marge

            temps_attente_entre_deux_activites = debut_act_suivante - fin_act_actuelle
            utilite_temp_attente += 3000*max(0,temps_attente_entre_deux_activites - temps_trajet) #On penalise plus le temps d'attente
            
            if(i == len(planing_activite_deux_jours) - 1):
                utilite_cout += (planing_activite_deux_jours[i+1].activity.Price[jour_timestamp])*2
                utilite_marge += (planing_activite_deux_jours[i+1].activity.margin[jour_timestamp])*10
                
        self.note = int(utilite_jour_vide + utilite_nb_act + utilite_marge - utilite_temps_trajet/3600 - utilite_temp_attente/3600 - utilite_cout) #On renvoie la note du planning
        #print("nb activite :",len(planing_activite_deux_jours))
        #print("utilite_nb_act :",utilite_nb_act)
        #print("utilite_marge :",utilite_marge)
        #print("utilite_temps_trajet :",utilite_temps_trajet)
        #print("utilite_temp_attente :",utilite_temp_attente)
        #print("utilite_cout :",utilite_cout)
        return self.note


    
    ##==========================================================================================
    #  MUTATIONS
    ##==========================================================================================
    
    def mutation_deletion(self):
        
        planning = self.liste_enfant_planning
        if(len(planning) > 1):        
            indice_random = random.randint(0, len(planning)-1)
            
            self.liste_id_dispo_suite.append(self.liste_enfant_planning[indice_random].activity.Id)

            if (indice_random==0): #Premier cas : lactivité retirée est la premiere
                temp1 = self.liste_enfant_planning[1].activity.localisation[0]
                temp2 = self.liste_enfant_planning[1].activity.localisation[1] 
                loc_1 = self.lieu_depart["latitude"]
                loc_2 = self.lieu_depart["longitude"] #On calcule le temps trajet depuis le lieu de départ
                temps_trajet_maison_act = temps_de_trajet_deux_activites(temp1, temp2, loc_1, loc_2, self.mode_transport)
                self.liste_enfant_planning[1].temps_act_precedente = temps_trajet_maison_act
                planning.pop(0)
            elif(indice_random == len(planning) - 1): #deuxieme cas cest la derniere (pas de temps de trajet) a gerer
                planning.pop(-1)   
            else: #Cas general on enleve i du coup il faut reconnecter i-1 et i+1 au niveau des temps de trajets et on est pas dans le cas
            #ou i est le derrnier element. Du coup i-1 et i+1 existent forcement sinon i serait egal à len(planning)-1
                temp1 = self.liste_enfant_planning[indice_random-1].activity.localisation[0] 
                temp2 = self.liste_enfant_planning[indice_random-1].activity.localisation[1]   
                temp3 = self.liste_enfant_planning[indice_random+1].activity.localisation[0] 
                temp4 = self.liste_enfant_planning[indice_random+1].activity.localisation[1]    
                temp_trajet = temps_de_trajet_deux_activites(temp1, temp2, temp3, temp4, self.mode_transport)
                self.liste_enfant_planning[indice_random+1].temps_act_precedente = temp_trajet  
                planning.pop(indice_random)
            #remettre a jour temps de trajet avec 
            self.liste_enfant_planning = planning
        else:
            self.liste_enfant_planning = []
        return 

    def mutation_par_insertion(self, activity):

        enfant_planing = enfant_planning(0,activity,0,0)
        planing = self.liste_enfant_planning

        temp1 = enfant_planing.activity.localisation[0] # localisation de l'activité qu'on veut insérer
        temp2 = enfant_planing.activity.localisation[1] 

        loc_1 = self.lieu_depart["latitude"]
        loc_2 = self.lieu_depart["longitude"]

        temps_trajet_maison_act = temps_de_trajet_deux_activites(temp1, temp2, loc_1, loc_2, self.mode_transport)

        blank_activity_start = enfant_planning(0,activity,0,0) # Sert a faire des comparaison en segments
        blank_activity_start.nombre_unites = 0
        planing.insert(0,blank_activity_start)

        blank_activity_end = enfant_planning(1440 * len(self.jour)*60,activity,0,0)
        blank_activity_end.nombre_unites = 0
        planing.append(blank_activity_end)
        
        for m in range(len(activity.liste_de_jours)):
            debut_jour = 1440*m + int(self.heure_debut_journee/60)
            if int(activity.liste_de_jours[m]) != -m:  
                for j in range(len(activity.list_begin_hours[m])):

                    if(activity.visite_libre):

                        start_activity = int(int(activity.list_begin_hours[m][j][0])/60)  # debut de l'activité que l'on veut inserer
                        end_activity =  int(int(activity.list_begin_hours[m][j][1])/60)  # fin de l'activité que l'on veut inserer
                        duree = enfant_planing.nombre_unites

                    else:                      
                        start_activity =  int(int(activity.list_begin_hours[m][j])/60)
                        duree = enfant_planing.nombre_unites
                        
                        enfant_planing.debut_activity = start_activity + 1440*m  
                        start_activity = enfant_planing.debut_activity              
                        end_activity = start_activity + duree
                     # activté qu'on veut insérer

                    for i in range(len(planing)-1):

                        fin_activite = planing[i].debut_activity + planing[i].nombre_unites # fin activité i
                        debut_activite = planing[i+1].debut_activity # debut activité i+1
                        borne_inf = max(fin_activite, start_activity) #dans le cas d'un musée : 
                        
                        temp3 = planing[i].activity.localisation[0] # localisation de l'activité i
                        temp4 = planing[i].activity.localisation[1]   

                        #temp_trajet = 0                  
                        temp_trajet = temps_de_trajet_deux_activites(temp1, temp2, temp3, temp4, self.mode_transport)
                        temp_tr0 = temp_trajet

                        if(activity.visite_libre):

                            if(borne_inf + temp_trajet + duree <= debut_activite): #Si cest un musée On peut l'inserer nimporte quand dans l'intervalle borne sup borne inf                 
                                start_activity = borne_inf + temp_trajet                   
                                end_activity = start_activity + duree
                            else:
                                start_activity = 1440 * len(self.jour) #Si cest pas le cas on s'assure qu'on ne l'insere pas
                                end_activity = start_activity + duree

                        if(debut_jour+temps_trajet_maison_act<=start_activity):
                            if(fin_activite + abs(temp_trajet) <= start_activity): # Si la fin de l'acivité i + le temps de trajet est inférieur au début de l'activité que l'on veut insérer
                                enfant_planing.temps_act_precedente = temp_trajet
                                
                                temp3 = planing[i+1].activity.localisation[0]
                                temp4 = planing[i+1].activity.localisation[1] 

                                #temp_trajet = 0 
                                temp_trajet = temps_de_trajet_deux_activites(temp1,temp2,temp3,temp4,self.mode_transport)
                                temp_tr1 = temp_trajet
                                if(end_activity + abs(temp_trajet) <= debut_activite): #If temps de trajet coherent : si la fin de l'activité que l'on veut insérer + le temps de trajet est inférieur au debut de l'activité i
                                    planing[i+1].temps_act_precedente=temp_trajet
                                    
                                    enfant_planing.jour = int(self.jour[m])
                                
                                    planing.pop(-1)
                                    enfant_planing.debut_activity = start_activity
                                    
                                    planing.pop(0)
                                    planing.insert(i,enfant_planing)
                                    self.liste_enfant_planning = planing 

                                    return True
        planing.pop(0)
        planing.pop(-1)
        
        return False

##==========================================================================================
# Calcul du temps entre deux activités
##==========================================================================================

def temps_de_trajet_deux_activites(latitude_1, longitude_1, latitude_2, longitude_2, mode_transport):
    distance = distance_deux_activites(latitude_1, longitude_1, latitude_2, longitude_2)
    if (mode_transport == "transit"):
        return (distance/4)*3600 + 5*60
    elif (mode_transport == "driving"):
        return (distance/80 )*3600 + 5*60

            
##==========================================================================================
# Calcul de la distance entre deux activités
##==========================================================================================

def distance_deux_activites(latitude_1, longitude_1, latitude_2, longitude_2):
    latitude_1 = radians(float(latitude_1))
    longitude_1 = radians(float(longitude_1))
    latitude_2 = radians(float(latitude_2))
    longitude_2 = radians(float(longitude_2))
    dist_radian = 6371*acos(sin(latitude_1)*sin(latitude_2) + cos(latitude_1)*cos(latitude_2)*cos(longitude_1 - longitude_2))#en km
    return dist_radian
