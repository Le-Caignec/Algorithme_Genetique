from datetime import datetime
from datetime import timezone

retour_dico1 = {'01828e94-e056-11e9-839b-0cc47a0803e4': {'attr': '01828e94-e056-11e9-839b-0cc47a0803e4', 'json_schedule': {'earlyArrival': '900', 'lastArrival': '', 'delayBeforeEndingHour': False, 'duration': 10800, 'isNotLimited': False}, 'json_scheduling': [{'annualPeriod': {'start': 1607295600, 'end': 1635458400}, 'days': [3], 'openingHours': [{'start': 56400, 'end': 67200}]}, {'annualPeriod': {'start': '1607295600', 'end': '1634508000'}, 'days': [1], 'openingHours': [{'start': '56400', 'end': '67200'}]}, {'annualPeriod': {'start': '1607295600', 'end': '1635112800'}, 'days': [5], 'openingHours': [{'start': '56400', 'end': '67200'}]}, {'annualPeriod': {'start': '1616968800', 'end': '1635112800'}, 'days': [4], 'openingHours': [{'start': '56400', 'end': '67200'}]}, {'annualPeriod': {'start': '1617573600', 'end': '1635112800'}, 'days': [2], 'openingHours': [{'start': '56400', 'end': '67200'}]}], 'json_price': {'isFree': False, 'currency': 'EUR', 'margin': '', 'marginRate': 25, 'marge': None}, 'json_pricing': [{'pricingPeriod': {'start': 1607295600, 'end': 1635458400}, 'individualRules': [{'type': '', 'id': 'Visite en anglais-Tarif standard (8+)-(standard-price)', 'name': 'Tarif standard (8+)-(standard-price)', 'price': '69', 'minAge': '', 'maxAge': ''}]}, {'pricingPeriod': {'start': 1607295600, 'end': 1635458400}, 'individualRules': [{'type': '', 'id': 'Visite en français-Tarif standard (8+)-(standard-price)', 'name': 'Tarif standard (8+)-(standard-price)', 'price': '69', 'minAge': '8', 'maxAge': '100'}]}, {'pricingPeriod': {'start': 1607295600, 'end': 1635458400}, 'individualRules': [{'type': '', 'id': 'Visite en allemand-Tarif standard (8+)-(standard-price)', 'name': 'Tarif standard (8+)-(standard-price)', 'price': '69', 'minAge': '', 'maxAge': ''}]}, {'pricingPeriod': {'start': 1607295600, 'end': 1635458400}, 'individualRules': [{'type': '', 'id': 'Visite en italien-Tarif standard (8+)-(standard-price)', 'name': 'Tarif standard (8+)-(standard-price)', 'price': '69', 'minAge': '', 'maxAge': ''}]}, {'pricingPeriod': {'start': 1607295600, 'end': 1635458400}, 'individualRules': [{'type': '', 'id': 'Visite en espagnol-Tarif standard (8+)-(standard-price)', 'name': 'Tarif standard (8+)-(standard-price)', 'price': '69', 'minAge': '', 'maxAge': ''}]}], 'postal_code': '50129', 'address_locality': 'Florence', 'address_country': 'IT', 'street_address': 'Via Cavour 92,', 'latitude': '43.7814251', 'longitude': '11.26106870000001'}}

retour_dico2 = {'0984ae63-5d2f-11e8-8390-02420a000106': {'attr': '0984ae63-5d2f-11e8-8390-02420a000106', 'json_schedule': {'earlyArrival': 900, 'lastArrival': 25200, 'delayBeforeEndingHour': 0, 'duration': 18000, 'isNotLimited': False}, 'json_scheduling': [{'annualPeriod': {'start': 1609459200, 'end': 1640908800}, 'days': [1, 2, 3, 4, 5, 6, 7], 'openingHours': [{'start': 21600, 'end': 50400}]}], 'json_price': {'isFree': '', 'currency': 'EUR', 'margin': '', 'marginRate': '10'}, 'json_pricing': [{'pricingPeriod': {'start': 1606777200, 'end': 1640905200}, 'individualRules': [{'type': 'individual', 'id': '7e85ef41-7ad7-11e8-8390-02420a000106', 'name': 'Tous', 'price': '55.00', 'minAge': '8', 'maxAge': '70'}]}], 'postal_code': None, 'address_locality': 'Santa Marta', 'address_country': 'CO', 'street_address': 'Vías Parque Nacional Tayrona, Santa Marta, Magdalena', 'latitude': '11.281225', 'longitude': '-73.91475300000002'}, '18b15cca-0f87-11ea-bbfb-0cc47a0803e4': {'attr': '18b15cca-0f87-11ea-bbfb-0cc47a0803e4', 'json_schedule': {'earlyArrival': 1200, 'lastArrival': False, 'delayBeforeEndingHour': 0, 'duration': 32400, 'isNotLimited': False}, 'json_scheduling': [{'annualPeriod': {'start': 1572566400, 'end': 1635638400}, 'days': [1, 5], 'openingHours': [{'start': 28800, 'end': 61200}]}], 'json_price': {'isFree': '', 'currency': 'MUR', 'margin': '', 'marginRate': '20'}, 'json_pricing': [{'pricingPeriod': {'start': 1572562800, 'end': 1635631200}, 'individualRules': [{'type': 'individual', 'id': '18b17bf4-0f87-11ea-bbfb-0cc47a0803e4', 'name': 'Enfant', 'price': '1625.00', 'minAge': '2', 'maxAge': '12'}, {'type': 'individual', 'id': '18b17ffe-0f87-11ea-bbfb-0cc47a0803e4', 'name': 'Adulte', 'price': '3250.00', 'minAge': '13', 'maxAge': '100'}]}], 'postal_code': None, 'address_locality': 'Curepipe', 'address_country': 'MU', 'street_address': None, 'latitude': '-20.3170872', 'longitude': '57.52652890000002'}}


##==========================================================================================
# Fonctions de récupérations des dates et des données
##==========================================================================================

def recup_duration_days_hours(dico):
    recup = []
    for act_id in dico.keys() :
        retouri = {}
        retouri['attr'] = act_id
        duration = dico[act_id]['json_schedule']['duration']
        retouri['duration'] = duration
        openingHours = dico[act_id]['json_scheduling'][0]['openingHours']
        retouri['openingHours'] = openingHours
        days = dico[act_id]['json_scheduling'][0]['days']
        retouri['days'] = days
        retouri['json_scheduling'] = dico[act_id]['json_scheduling']
        recup.append(retouri)
    return recup


##==========================================================================================
# Fonctions de tests sur le type d'activités
##==========================================================================================
 
def test_activite_bon_horaires(dico, duration): # Permet de savoir si les données de l'activite sont bonnes 
    if int(duration) + int(dico["json_scheduling"][0]["openingHours"][0]["start"]) > int(dico["json_scheduling"][0]["openingHours"][0]["end"]):
        return False
    else:
        return True

def visite_libre_ou_non(dico, duration): # Fonction qui prend un dico correspondant a une activité et qui retourne si une activité est de type visite_libre ou non
    if int(duration) + int(dico["json_scheduling"][0]["openingHours"][0]["start"]) == int(dico["json_scheduling"][0]["openingHours"][0]["end"]):
        return False
    else:
        return True
        
def retourne_jour_int(secondes): #Retourne le jour : 1 pour lundi, 6 pour samedi
    return (int(list(datetime.fromtimestamp(secondes).isocalendar())[2]))

def test_pause_dejeuner_visite_non_libre(start, end, pause_dejeuner):
    if pause_dejeuner:     
        if((int(start) >= 50400 or int(end) <= 43200) and (start < end)): #début>14h ou fin<12h
            return True
        else:
            return False
    return True

def test_pause_dejeuner_visite_libre(temp, duration):
    objet = []                                
    if ((temp[0] < 43200) and (43200 < temp[1] < 50400) and (temp[0] + duration <= 43200)): #début<12h et 12<fin<14
        temp[1] = 43200
    elif ((temp[0] < 43200) and (temp[1] > 50400)): #début<12h et fin>14h
        if 43200 - duration >= temp[0]:
            objet.append([temp[0],43200])
        if 50400 + duration <= temp[1]:
            objet.append([50400,temp[1]])
        else:
            temp = []
    elif ((43200 < temp[0] < 50400) and (43200 < temp[1] < 50400)): #12h<début<14h et 12h<fin<14h
        temp = []
    elif ((43200 < temp[0] < 50400) and (temp[1] > 50400) and (50400 + duration <= temp[1])): #12h<début<14h et fin>14h
        temp[0] = 50400
    return objet, temp
##==========================================================================================
# Creation du pool d'activité fille correspondant au planning du visiteur
##==========================================================================================

#Modifications possibles vis-a-vis de la liste des jours 
#12 h = 43200
#14 h = 50400
def creation_debut_act_fille(recup, liste_jours_user, début_journée_user, pause_dejeuner): #recup = dico de dico, liste = timestamp des 2 jours
    essai = {}   
    for act_id in recup.keys():    
        duration = recup[act_id]["json_schedule"]["duration"]
        if(test_activite_bon_horaires(recup[act_id], duration)): #on fait le test que l'horaire de l'act est bon
        
            dico_act_fille_i = {}  
            indice = 0         
            #On met un jour != None car on pourra faire un planing sur un seul jour.      
            for jour in liste_jours_user: 
                indice -=1
                booleen = True   
                dico_act_fille_i[str(indice)] = []        
                if jour != None: #On va comparer la liste des jours de l'utilisateur avec annual période et days                                       
                    #Dico contenant visite_libre et les listes d'horaires en fonction des jours
                    if(visite_libre_ou_non(recup[act_id], duration)): #renvoie true si c'est une activité de type visite libre                                   
                        dico_act_fille_i["visite_libre"] = True                                     
                    else:
                        dico_act_fille_i["visite_libre"] = False
                    for schedules in recup[act_id]["json_scheduling"]:
                        #On compare si le timestamp de l'utilisateur est compris dans la période donnée
                        start_period = schedules['annualPeriod']['start']
                        end_period = schedules['annualPeriod']['end']
                        dico_act_fille_i["duration"] = duration
                        if((int(jour) >= int(start_period)) and (int(jour) <= int(end_period))):#Pour savoir si le jour est dans la période
                            jour_semaine_correspondant = retourne_jour_int(jour) #On traduit le timestamp en 1 2 3 4 5 6 7
                            for jour_disponible in schedules["days"]:
                                #Si le jour demandé par l'utilisateur est dispo le jour de sa période alors on fait un pool d'activité
                                if (jour_semaine_correspondant == jour_disponible): #Si c'est bon, on y rentre  
                                    horaires = []                                 
                                    for j in range(len(schedules["openingHours"])):     
                                        if len(horaires)>0:                              
                                            dico_act_fille_i[str(jour)] = horaires
                                        if len(horaires)> 0 and booleen:
                                            booleen = False
                                            del dico_act_fille_i[str(indice)]                                                                        
                                        openingHours_start = schedules["openingHours"][j]["start"]
                                        openingHours_end = schedules["openingHours"][j]["end"] 
                                        if (dico_act_fille_i["visite_libre"]):                                    
                                            openingHours_start = max(début_journée_user,openingHours_start)
                                            temp = [openingHours_start,openingHours_end]       
                                            if pause_dejeuner: #Faire des cas pour adapter les horaires en fonction de la présence d'un temps libre entre 12h et 14h 
                                                liste_horaires, temp = test_pause_dejeuner_visite_libre(temp, duration)
                                                if len(liste_horaires) == 0:
                                                    horaires.append(temp)
                                                else:
                                                    for temps in liste_horaires:
                                                        horaires.append(temps)
                                            else:
                                                horaires.append(temp)
                                            if len(horaires)>0:                              
                                                dico_act_fille_i[str(jour)] = horaires
                                            if len(horaires)> 0 and booleen:
                                                booleen = False
                                                del dico_act_fille_i[str(indice)] 
                                        else:                                         
                                            if (int(début_journée_user) <= int(schedules["openingHours"][j]["start"])):
                                                openingHours_start = schedules["openingHours"][j]["start"]                                                                          
                                                #Indice 0 cest le debut de l'act et 1 cest la durée                                              
                                                if (test_pause_dejeuner_visite_non_libre(openingHours_start, openingHours_end, pause_dejeuner)):
                                                    horaires.append(openingHours_start)
                                                    #On empeche les visites fixe de se mettre entre midi et 2 si on a une pause dejeuner
                                                    if len(horaires)>0:                              
                                                        dico_act_fille_i[str(jour)] = horaires
                                                    if len(horaires)> 0 and booleen:
                                                        booleen = False
                                                        del dico_act_fille_i[str(indice)]  
        #if(len(dico_act_fille_i.keys()) !=4):
            #print("Deso j'ai menti ca marche po lol")                                                    
        essai[act_id] = dico_act_fille_i #On forme le dico de dico de bool et listes                                     
    return essai


def datetime_en_timestamp(date):
    return int(datetime.strptime(date, '%d/%m/%Y').replace(tzinfo = timezone.utc).timestamp())

def decoupage_sejour(liste_dates): #début = [0]
    date_debut_secondes = datetime_en_timestamp(liste_dates[0])
    date_fin_secondes = datetime_en_timestamp(liste_dates[1])
    date_debut_variable = date_debut_secondes
    un_jour = 86400
    deux_jours = 172800 #2 jours en secondes
    liste_creneaux_jours = []
    if date_debut_secondes == date_fin_secondes:
        return [[date_debut_secondes]]
    while date_debut_variable + un_jour <= date_fin_secondes:
        liste_creneaux_jours.append([date_debut_variable, date_debut_variable + un_jour])
        date_debut_variable += deux_jours
    if date_debut_variable + deux_jours > date_fin_secondes and liste_creneaux_jours[len(liste_creneaux_jours)-1][1] != date_fin_secondes:
        liste_creneaux_jours.append([date_fin_secondes])
    return liste_creneaux_jours #Retourne [[Jour11Timestamp, Jour12Timestamp], [Jour21Timestamp, Jour22Timestamp], ...], la dernière liste peut ne contenir qu'un seul élément

#print(creation_debut_act_fille(retour_dico2,[1623013200,1625816775],32400))

