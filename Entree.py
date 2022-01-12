import json
import os, sys
from time import *
from urllib.parse import unquote
import re
from recupActivitiesMother import *
#from GUI import *
#from Generations import *

##==========================================================================================
# Récupération dans une liste des ids sélectionnés par l'utilisateur
##==========================================================================================

def recup_ids(json_entree):
    list_id=json_entree["data"]["select"]
    return list_id


##==========================================================================================
# Recupération des coordonnées GPS du point de départ
##==========================================================================================

#
def recup_area(json_entree):
    GPS={}
    GPS["latitude"] = json_entree["data"]["area"].split(',')[0]
    GPS["longitude"] = json_entree["data"]["area"].split(',')[1]
    return GPS

##==========================================================================================
# Récupération des données qui nous interessent (le pays, ville, période du séjour, nombre de passagers, leur date de naissance)
##==========================================================================================
  
def recup_search(json_entree):
    txt=json_entree["data"]["search"]
    txt = unquote(txt)
    txt=txt.replace("start=1&data", '')
    txt=txt.replace("[", '')
    txt=txt.replace("]", '')
    list=re.split("&data|&",txt)
    infos_utilisateurs={}
    dico={}
    for i in range (len(list)):
        list[i]=list[i].split("=")
        if (list[i][0]=="pays"):
            infos_utilisateurs[list[i][0]]=list[i][1]
        elif (list[i][0]=="passengers"):
            infos_utilisateurs[list[i][0]]=list[i][1]
        elif (list[i][0]=="dates"):
            list[i][1]=list[i][1].split("+-+")
            infos_utilisateurs[list[i][0]]=list[i][1]
        elif (list[i][0]=="ville"):
            infos_utilisateurs[list[i][0]]=list[i][1]
        elif (re.search("input",list[i][0])):
                dico["passenger_" + list[i][0][5]] = list[i][1]
    infos_utilisateurs["dates_naissances_passagers"] = dico
    return infos_utilisateurs

##==========================================================================================
# Récupération du type de transport choisi sous forme de string
##==========================================================================================

def recup_mode(json_entree):
    return json_entree["mode"]

##==========================================================================================
# Renvoie un booléen b=True si l'utilisateur veut une pause dej et False sinon
##==========================================================================================


def recup_dinner(json_entree):
    b=False
    if (json_entree["dinner"]=='1'):
            b=True
    return b

##==========================================================================================
# Récupération de l'heure de début de journée que l'utilisateur souhaite
##==========================================================================================

def recup_plusHour(json_entree):
    return int(json_entree["plushour"])

