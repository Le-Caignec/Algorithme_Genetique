## IMPORTS
from activity import *

##==========================================================================================
# CLASSE ENFANT_PLANNING
##==========================================================================================

class enfant_planning:

    def __init__(self, debut_activity, activity, temps_act_precedente, jour):
        self.debut_activity = (float(debut_activity)/60) # en minutes
        self.activity = activity
        self.nombre_unites = int(self.activity.duration/60) # en minutes
        self.temps_act_precedente = temps_act_precedente 
        self.jour = jour #jour sur lequel est placé l'activité en timstamp

    def affichage_enfant_planning(self):
        print("------------------------ENFANT PLANNING------------------------")
        print("Heure de début d'une activité : ", self.debut_activity)
        print("nombre d'unité qu'une activité prend : ", self.nombre_unites)
        print("Jour sur lequel est placé l'activité : ",self.jour)
        print("Objet Activity : ")
        print(self.activity.affichage_activity())
        return 
    