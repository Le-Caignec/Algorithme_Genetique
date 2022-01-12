from __future__ import print_function
from datetime import datetime
import os.path
from planning_jour import planning_jour
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from planning_jour import *
from Entree import *

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

##==========================================================================================
# Permet de créer une connection au calandrier et à l'API google
##==========================================================================================

def connection():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_690666056398-h8sn95prtj7uosnichuress6t1c8bdei.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)    

    return service

##==========================================================================================
# Permet de convertir un timestamp en utc = +00:00
##==========================================================================================

def conversion_timestamp_utc(timestamp, utc = "+00:00"): # utc = "+00:00"
    date_test = datetime.utcfromtimestamp(timestamp).isoformat() + utc
    return date_test

##==========================================================================================
# Retourne l'id du calendrier ayant un nom donnée
##==========================================================================================

def list_calendar_find_id(service, name_calendar): # Retourne l'id du calendrier ayant ce nom
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if (calendar_list_entry['summary']== name_calendar):
                return calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

##==========================================================================================
# Créer un calendrier et retourne son id / supprime un calandrier
##==========================================================================================

def create_calendar(service, name_calendar): # Crée un calendrier et retourne l'id du calendrier crée (en fonction d'un nom donné en paramètre)
    calendar = {
        'summary': name_calendar,
        'timeZone': 'Europe/Paris'
    }
    service.calendars().insert(body=calendar).execute()
    id_new_calendar=list_calendar_find_id(service, name_calendar)
    return id_new_calendar

def del_calendar(service, name_calendar): # Suppression calendrier (depuis un nom de calendrier)
    id_calendar_to_delete = list_calendar_find_id(service, name_calendar)
    service.calendars().delete(calendarId=id_calendar_to_delete).execute()


##==========================================================================================
# Ajoute des événement dans un calandrier et supprime des évènements 
##==========================================================================================
def add_events(service, idCalendar, idActivity, timestamp_debut, timepstamp_fin): # Ajoute un evenement dans un calendrier
    
    event = {
        'summary': idActivity,
        'start': {
            'dateTime': timestamp_debut,
            'timeZone': 'Europe/Paris',
        },
        'end': {
        'dateTime': timepstamp_fin,
        'timeZone': 'Europe/Paris',
         },
    }

    event = service.events().insert(calendarId=idCalendar, body=event).execute()
    return 

def del_all_events_in_calendar(service, names_calendar): 
    list_id_calendar=[]
    for name in names_calendar:
        id_calendar = list_calendar_find_id(service, name)
        list_id_calendar.append(id_calendar)
    for id_calendar in list_id_calendar:
        page_token = None
        while True:
            events_list = service.events().list(calendarId=id_calendar, pageToken=page_token).execute()
            for event in events_list['items']:
                service.events().delete(calendarId=id_calendar, eventId=event['id']).execute()
            page_token = events_list.get('nextPageToken')
            if not page_token:
                break
##==========================================================================================
# Recupération de toutes les activites
##==========================================================================================
def recup_horaires_planning(planning): # Recuperer dans un tableau : [[id, debut, fin],...] de chaque activité dans un planning
    list_activites_planning = [] 
    for i in range(len(planning.liste_enfant_planning)):
        if (planning.liste_enfant_planning[i].debut_activity*60 > 86399):
            debut_activite = (planning.liste_enfant_planning[i].debut_activity - 1440)*60 + planning.liste_enfant_planning[i].jour
            fin_activite = (planning.liste_enfant_planning[i].debut_activity - 1440)*60 + planning.liste_enfant_planning[i].nombre_unites*60 + planning.liste_enfant_planning[i].jour
        else:
            debut_activite = (planning.liste_enfant_planning[i].debut_activity)*60 + planning.liste_enfant_planning[i].jour
            fin_activite = (planning.liste_enfant_planning[i].debut_activity)*60 + planning.liste_enfant_planning[i].nombre_unites*60 + planning.liste_enfant_planning[i].jour
        
        id_activite = planning.liste_enfant_planning[i].activity.Id
        list_activites_planning.append([id_activite, debut_activite, fin_activite]) # tableau avec id, debut et fin
    return list_activites_planning 


def remplissage_calendar(service, list_activites_planning, name): # Remplir le calendrier pour chaque activité dans une liste de planning
    id_calendar = list_calendar_find_id(service, name)
    for i in range (len(list_activites_planning)): # Pour chaque activites d'un planning 
        id = list_activites_planning[i][0] # id de l'activité (correspondra au nom ET à l'id d'un evenement dans la calendrier google)
        debut = conversion_timestamp_utc(list_activites_planning[i][1], "+00:00") 
        fin = conversion_timestamp_utc(list_activites_planning[i][2], "+00:00")
        add_events(service, id_calendar, id, debut, fin)

def remplissage_calendar_trajet(service, list_tmps_trajet, name): # Remplir le calendrier pour chaque activité dans une liste de planning
    id_calendar = list_calendar_find_id(service, name)
    j=0
    while j < len(list_tmps_trajet):
        if (list_tmps_trajet[j][0]==list_tmps_trajet[j][1]):
            del list_tmps_trajet[j]
        j+=1
    for i in range (len(list_tmps_trajet)): # Pour chaque activites d'un planning
        id="Temps de trajet" 
        debut = conversion_timestamp_utc(list_tmps_trajet[i][0], "+00:00") 
        fin = conversion_timestamp_utc(list_tmps_trajet[i][1], "+00:00")
        add_events(service, id_calendar, id, debut, fin)


##==========================================================================================
# Recupération des temps de trajet
##==========================================================================================

def recup_temps_trajet_planning(planning, json_entree): # Recuperer dans un tableau : [[debut, fin],...] de chaque activité dans un planning
    list_temps_trajet = []
    premier_act_premier_jour = True # False si c'est pas la première activité
    premier_act_deuxieme_jour = True # False si c'est pas la première activité
    for i in range(len(planning.liste_enfant_planning)):
        if (planning.liste_enfant_planning[i].debut_activity < 1440): # si c'est le 1er jour
            if (premier_act_premier_jour): # si c'est la première activité du premier jour
                fin = recup_plusHour(json_entree) + planning.liste_enfant_planning[i].jour # Fin de l'activité en secondes
                temps_trajet = float(temps_de_trajet_deux_activites(recup_area(json_entree)["latitude"], recup_area(json_entree)["longitude"], planning.liste_enfant_planning[i].activity.localisation[0], planning.liste_enfant_planning[i].activity.localisation[1], recup_mode(json_entree)))
                debut_tps_trajet = fin #Fin de l'activité en secondes pour 1 jour
                fin_tps_trajet = debut_tps_trajet + temps_trajet #La fin du trajet en secondes dans 1 jour
                premier_act_premier_jour = False
            else: 
                temps_trajet = float(temps_de_trajet_deux_activites(planning.liste_enfant_planning[i-1].activity.localisation[0], planning.liste_enfant_planning[i-1].activity.localisation[1], planning.liste_enfant_planning[i].activity.localisation[0], planning.liste_enfant_planning[i].activity.localisation[1], recup_mode(json_entree)))
                fin = planning.liste_enfant_planning[i].jour + planning.liste_enfant_planning[i-1].debut_activity*60 + planning.liste_enfant_planning[i-1].nombre_unites*60
                debut_tps_trajet = fin
                fin_tps_trajet = debut_tps_trajet + temps_trajet
        else:
            if (premier_act_deuxieme_jour): # si c'est la première activité du 2ème jour 
                fin = recup_plusHour(json_entree) + planning.liste_enfant_planning[i].jour # Fin de l'activité en secondes
                temps_trajet = float(temps_de_trajet_deux_activites(recup_area(json_entree)["latitude"], recup_area(json_entree)["longitude"], planning.liste_enfant_planning[i].activity.localisation[0], planning.liste_enfant_planning[i].activity.localisation[1], recup_mode(json_entree)))
                debut_tps_trajet = fin #Fin de l'activité en secondes pour 1 jour
                fin_tps_trajet = debut_tps_trajet + temps_trajet #La fin du trajet en secondes dans 1 jour
                premier_act_deuxieme_jour = False
            else: 
                temps_trajet=float(temps_de_trajet_deux_activites( planning.liste_enfant_planning[i-1].activity.localisation[0],planning.liste_enfant_planning[i-1].activity.localisation[1], planning.liste_enfant_planning[i].activity.localisation[0], planning.liste_enfant_planning[i].activity.localisation[1], recup_mode(json_entree))) 
                fin = planning.liste_enfant_planning[i].jour + (planning.liste_enfant_planning[i-1].debut_activity*60- 1440*60) + planning.liste_enfant_planning[i-1].nombre_unites*60
                debut_tps_trajet = fin  
                fin_tps_trajet = debut_tps_trajet + temps_trajet
            
        list_temps_trajet.append([float(debut_tps_trajet), float(fin_tps_trajet)]) # tableau debut et fin pour les temps de trajet```
    return list_temps_trajet

##==========================================================================================
# FONCTION PRINCIPALE
##==========================================================================================

def creation_calendriers(generation_jour, name_calendars): 
    service = connection()
    del_all_events_in_calendar(service, ["meilleur", "aléatoire 1", "aléatoire 2","aléatoire 3","aléatoire 4"])
    list_calendar= []
    i = 0
    for planning in generation_jour.generation_journees:
        list_calendar.append(recup_horaires_planning(planning)) # Recuperation des tableaux d'activités pour chaque planning
        remplissage_calendar (service, list_calendar[i], name_calendars[i]) # Placement des activité de chaque planning dans la calendrier google
        i = i + 1

#trace les temps de trajet associé à un planning 
def test_calandrier(planning, name, json_entree): 
    service = connection()
    list_calendar= []
    list_temps_trajet = []
    list_calendar.append(recup_horaires_planning(planning)) # Recuperation des tableaux d'activités pour chaque planning
    list_temps_trajet.append(recup_temps_trajet_planning(planning,json_entree))
    for i in range (len(list_calendar)):
        remplissage_calendar (service, list_calendar[i], name) # Placement des activités de chaque planning dans la calendrier google
        remplissage_calendar_trajet (service, list_temps_trajet[i],"Temps de Trajet")

##==========================================================================================
# FONCTION PRINCIPALE POUR LA FIN DU PROJET (affichage du planning entier)
##==========================================================================================

def affichage_algo_genetique(generation_totale, json_entree): 
    service = connection()
    del_all_events_in_calendar(service, ["meilleur", "aléatoire 1", "aléatoire 2","aléatoire 3","aléatoire 4","Temps de Trajet"]) #Vide les agendas
    list_calendar = []
    list_temps_trajet=[]
    i = 0
    for planning in generation_totale.List_planning:
        list_calendar.append(recup_horaires_planning(planning.generation_journees[0])) # Recuperation des tableaux d'activités pour chaque objet
        remplissage_calendar (service, list_calendar[i], "meilleur") # Placement des activité de chaque planning dans la calendrier google
        list_temps_trajet.append(recup_temps_trajet_planning(planning.generation_journees[0],json_entree))
        remplissage_calendar_trajet (service, list_temps_trajet[i],"Temps de Trajet")
        i = i + 1
    print("c'est bon j'ai bien affiché ton calendrier dans google calendar")
    
# aléatoire 1 : ije0vf60d44p6tct0es2msg6h8@group.calendar.google.com
# meilleur : egsg7pin4p70cfgum7a2hb2ojg@group.calendar.google.com
# 