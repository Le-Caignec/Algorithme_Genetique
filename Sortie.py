from recupActivitiesMother import *
from GUI_calandar import *
import json
import os
##==========================================================================================
# Retour du fichier JSON
##==========================================================================================

def ecriture_fichier_txt(json_sortie):
    if os.path.exists('sortie_API.json'):
        os.remove('sortie_API.json')
    with open('sortie_API.json', 'w', encoding='utf-8') as f:
        json.dump(json_sortie, f, ensure_ascii=False, indent=4)

def retour_API(generation_totale, dico_dicos, json_entree):
    json_sortie = []
    for generation_dune_periode in generation_totale.List_planning:
        list_activites_planning = generation_dune_periode.generation_journees[0].liste_enfant_planning 
        for activite in list_activites_planning: # activite est un enfant_planning
            temps_dico = {}
            temps_dico["id"] = activite.activity.Id
            temps_dico["openday"] = retourne_jour_int(activite.jour)
            for dico_annualPeriod in dico_dicos[activite.activity.Id]["json_scheduling"]:
                if (int(dico_annualPeriod["annualPeriod"]["start"]) <= int(activite.jour) <= int(dico_annualPeriod["annualPeriod"]["end"])) and (retourne_jour_int(activite.jour) in dico_annualPeriod["days"]):
                    temps_dico["startp"] = dico_annualPeriod["annualPeriod"]["start"]
                    temps_dico["endp"] = dico_annualPeriod["annualPeriod"]["end"]
                    hours = []
                    for i in range (len(dico_annualPeriod["openingHours"])):
                        dico_inter = {}
                        dico_inter["startj"] = dico_annualPeriod["openingHours"][i]["start"]
                        dico_inter["endj"] = dico_annualPeriod["openingHours"][i]["end"]
                        hours.append(dico_inter)
                    temps_dico["hours"] = hours
            temps_dico["earlyArrival"] = dico_dicos[activite.activity.Id]["json_schedule"]["earlyArrival"]
            temps_dico["duration"] = dico_dicos[activite.activity.Id]["json_schedule"]["duration"]
            temps_dico["latitude"] = dico_dicos[activite.activity.Id]["latitude"]
            temps_dico["longitude"] = dico_dicos[activite.activity.Id]["longitude"]
            temps_dico["debut-activites"] = activite.jour + activite.debut_activity*60
            temps_dico["fin-activites"] = activite.jour + (activite.debut_activity + activite.nombre_unites )*60
            json_sortie.append(temps_dico)
    return Serialisation(json_sortie)