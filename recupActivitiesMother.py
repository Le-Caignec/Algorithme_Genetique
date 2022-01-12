import mariadb
from mariadb import Error
from configparser  import ConfigParser
from datetime import datetime
import json

# Lecture du fichier de conf (user, mdp, port ..)
def read_db_config(filename = 'config.ini', section = 'sql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
   	    items = parser.items(section)
   	    for item in items :
             db[item[0]] = item[1]
    else :
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    if db.get("port") != None :
        port = db.get("port")
        db["port"] = int(port)
    return db

#Connexion a la BDD (variable conn)
def connect():
    conn = None
    db_conf = read_db_config()
    try :
        conn = mariadb.connect(** db_conf)
    except Exception as e :
        print(f"Error: {e}")
    finally :
        return conn
	#There is no finality, now send request

#Permet de créer un dictionnaire de dictionnaires contenant les activité mère
def creation_dico_de_dico(lignes_bdd): #lignes_bdd est une liste de tuple/liste
    rowDict = {}
    for act in lignes_bdd : 
        dict = {
            "attr" : act[0], #ID de l'activite
            "json_schedule" : json.loads(act[1]), #contient la duration cest tout
            "json_scheduling" : json.loads(act[2]),#contient les periodes annuelles d'ouverture (date de début/de fin, jours hebdomadaires d'ouverture, horaires d'ouvertures dans la journée)
            "json_price" : json.loads(act[3]), #prix et margin rate 
            "json_pricing" : json.loads(act[4]), #prix en fonction de l'age
            "postal_code" : act[5],
            "address_locality" : act[6],
            "address_country" : act[7],
            "street_address" : act[8],
            "latitude" : act[9],
            "longitude" : act[10]
        }
        #Ajout du dico nouvellement cree a la liste des dictionnaires
        rowDict[dict["attr"]] = dict
    return rowDict

#Requete dans la BDD qui permet de recuperer des dictionnaires correspondants aux id des activités demandées
def get_activity_by_id(conn, liste_id):
    try : 
        lignes_bdd=[]
        cursor = conn.cursor()
        requete = "SELECT attr, json_schedule, json_scheduling, json_price, json_pricing, postal_code, address_locality, address_country, street_address, latitude, longitude FROM data_data INNER JOIN(SELECT activity__address.postal_code,activity__address.address_locality,activity__address.address_country,activity__address.street_address,activity__address.activity_id,geo_coordinates.latitude,geo_coordinates.longitude FROM activity__address INNER JOIN geo_coordinates ON activity__address.geo_coordinates_id = geo_coordinates.id WHERE (geo_coordinates.latitude IS NOT NULL AND geo_coordinates.longitude IS NOT NULL) OR (activity__address.postal_code IS NOT NULL AND activity__address.address_locality IS NOT NULL AND activity__address.address_country IS NOT NULL AND activity__address.street_address IS NOT NULL AND activity__address.street_address NOT LIKE 'INCONNU%' AND activity__address.street_address !='')) AS temp ON data_data.attr=temp.activity_id"    
        requete+= " WHERE"     
        for i in range(len(liste_id)-1):              
            requete+= ' attr="'+liste_id[i]+'" OR'            
        requete +=' attr="'+liste_id[len(liste_id)-1]+'"'
        cursor.execute(requete)
        for i in range(len(liste_id)):
            temprow = cursor.fetchone()
            lignes_bdd.append(temprow)
#lignes_BDD est une liste de dico
    except Error as e :
        print(e)
    finally:
        cursor.close()
        dico_dicos=creation_dico_de_dico(lignes_bdd)
        return dico_dicos


#Permet d'afficher de manière lisible (en format Json) le dico de dicos obtenu
def Serialisation(dico_dicos):
    json_object={}
    json_object =json.dumps(dico_dicos, indent=4)  
    return json_object
