from recupActivitiesMother import *
from Entree import *
from Creation_activités_filles import *
from datetime import datetime

##==========================================================================================
# CLASSE activity
##==========================================================================================

class activity:

    def __init__(self, Id, Price, margin, localisation, list_begin_hours, liste_de_jours, duration, visite_libre):
        self.Id = Id
        self.Price = Price
        self.margin = margin
        self.localisation = localisation #liste[latitude, longitude]
        self.localisation_prec = None
        self.list_begin_hours = list_begin_hours #
        self.duration = duration
        self.liste_de_jours = liste_de_jours
        self.visite_libre = visite_libre
      
    def affichage_activity(self):
        print("----------------------------------------ACTIVITÉ----------------------------------------")
        print("ID : ", self.Id)
        print("Price : ", self.Price)
        print("Margin : ", self.margin)
        print("Localisation : ", self.localisation)
        print("Localisation précédente : ", self.localisation_prec)
        print("Heures de début : ", self.list_begin_hours)# si visite libre  : [[[heure_debut1Jour1, heure_fin1Jour1], [heure_debut2Jour1, heure_fin2Jour1]], [heure_debut1Jour2, heure_fin1Jour2], [heure_debut2Jour2, heure_fin2Jour2]]] sinon : [[heure_debut1Jour1,heure_debut2Jour1], [heure_debut1Jour2,heure_debut2Jour2]]
        print("Durée : ", self.duration)
        print("Liste de jours : ", self.liste_de_jours)
        print("Visite libre : ", self.visite_libre)
        return 

##==========================================================================================
# Détermination du prix
##==========================================================================================

def prix_par_jour(dico_dicos, id, json_entree):
    dico_prix_jours={}
    jour = decoupage_sejour(recup_search(json_entree)["dates"])
    for i in range(len(jour)):
        for k in range (len(jour[i])):
            dico_prix_jours[jour[i][k]]=Price(dico_dicos, id, json_entree,jour[i][k])
    return dico_prix_jours #Retourne un dico contenant comme clé le timestamp d'un jour et en valeur le prix associé

    
def Price(dico_dicos, id, json_entree, jour): 
    prix = 0
    nb_participants = recup_search(json_entree)["passengers"]
    list_ages = []
    for i in range(int(nb_participants)):
        born_str = recup_search(json_entree)["dates_naissances_passagers"]["passenger_" + str(i)]
        born = datetime.strptime(born_str, '%d/%m/%Y')
        date_du_jour = datetime.fromtimestamp(jour)   # On cree un objet de type datetime pour le comparer avec le delais mis en paramètres
        age = date_du_jour.year - born.year - ((date_du_jour.month, date_du_jour.day) < (born.month, born.day))
        list_ages.append(age)
    for k  in range(len(list_ages)):# on parcourt les ages des passagers
        b = False #Booleen qui passe a True si un prix a été trouvé pour la période horaire
        for j in range(len(dico_dicos[id]["json_pricing"])): # Parcours des pricing period
            debut = datetime.fromtimestamp(dico_dicos[id]["json_pricing"][j]["pricingPeriod"]["start"])
            if (debut <= date_du_jour): # si un jour de la periode choisie par l'utilisateur est supérieur à la date de début de la pricing period
                nb_grille_tarifaire = len(dico_dicos[id]["json_pricing"][j]["individualRules"])
                for i in range (nb_grille_tarifaire): # pour toutes les grilles tarifaires dans une pricing period
                    if ((dico_dicos[id]["json_pricing"][j]["individualRules"][i]["minAge"] != "") or (dico_dicos[id]["json_pricing"][j]["individualRules"][i]["maxAge"] != "")):
                        if ((float(dico_dicos[id]["json_pricing"][j]["individualRules"][i]["minAge"]) <= float(list_ages[k])) and (float(dico_dicos[id]["json_pricing"][j]["individualRules"][i]["maxAge"]) >= (float(list_ages[k])))):
                            prix = prix + float(dico_dicos[id]["json_pricing"][j]["individualRules"][i]["price"])
                            b = True
                            break
            if b:
                break
    return prix


##==========================================================================================
# Définition d'un dico  d'objet activité fille
##==========================================================================================

def dico_activité_fille(dico_dicos, json_entree, pool_act_filles):
    dico_fille = {}
    for key1 in pool_act_filles.keys(): #On est dans le dico correspondant aux dicos des activités, keys = act_id
        Id = key1
        price = prix_par_jour(dico_dicos, Id, json_entree)
        list_begin_hours = []
        liste_de_jours = []
        if ((pool_act_filles[key1]["duration"] != 0) or (pool_act_filles[key1]["duration"] != "0")):
            for key2 in pool_act_filles[key1].keys(): #On est dans le dico correspondant à une activité, keys = visite_libre, duration, ...
                if key2 == "duration":
                    duration = pool_act_filles[key1][key2]
                elif key2 == "visite_libre":
                    visite_libre = pool_act_filles[key1][key2]
                else: #On récupère la liste des horaires
                    list_begin_hours.append(pool_act_filles[key1][key2]) 
                    liste_de_jours.append(key2)
            localisation = []
            margin = {}
            for key in price.keys():
                if ((isinstance(dico_dicos[key1]["json_price"]["marginRate"],str)) and (dico_dicos[key1]["json_price"]["marginRate"]!="")):
                    margin[key] = ((float(dico_dicos[key1]["json_price"]["marginRate"]))/100)*price[key]
                else:
                    margin[key] = 0
            localisation.append(dico_dicos[key1]["latitude"])
            localisation.append(dico_dicos[key1]["longitude"])
            activity_fille = activity(Id, price, margin, localisation, list_begin_hours,liste_de_jours, duration, visite_libre)
            dico_fille[Id] = activity_fille
    return dico_fille #Dico d'activity utilisables pour faire un planning
