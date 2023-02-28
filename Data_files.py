from Lol_APP.main import *
import mysql.connector

#datos
values = ["tier","rank","summonerName","leaguePoints","wins","losses"]

a = estadisticas_ranked(region, jugador)

#diccionario con queries para interactuar con la base de datos
statements = {
    "get_player_ranked_data": "SELECT * FROM Ranked_Data WHERE summoner_name LIKE %s",
    "set_player_ranked_data": "INSERT INTO Ranked_Data (tier, rank, summoner_name, league_points, wins, losses) " 
                              "VALUES (%(tier)s, %(rank)s, %(summonerName)s, %(leaguePoints)s, %(wins)s, %(losses)s)" #Tengo que parametrizar de esta forma horrenda porque los datos a guardar están en un dict
    }

def get_dict(lista):
    """
    The get_dict function takes a list of dictionaries and returns a list of only dictionaries.
        
    :param lista: Iterate through the list
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    dictionar = []
    for elemento in lista:
        if isinstance(elemento, dict):
            dictionar.append(elemento)
    return dictionar
    

def extract_dict(var_array):
    """
    The extract_dict function extracts the dictionary from a list of dictionaries.
    It takes in a variable array and returns the first dictionary it finds.
    
    :param var_array: Store the data 
    :return: A dictionary
    :doc-author: Trelent
    """
    for i in range(len(var_array)):
        data = var_array[i]
    return data

def buscar_valor(data_dict,values):
    """
    The buscar_valor function takes a dictionary and a list of keys as input. It returns 
    a new dictionary with the same keys as the original, but with values that are either None or 
    the value associated to that key in the original dictionary. If there is no value for a given key, it will be set to None.
    
    :param data_dict: Store the data that is going to be searched
    :param values: Define the keys of the dictionary that will be returned
    :return: A dictionary with the keys that are in values and the respective values
    :doc-author: Trelent
    """
    dict = {}
    for key in values:
        if key in data_dict:
            dict[key] = data_dict[key]
    return dict

def connect_database():
    """
    Genera la conexión con la base de datos ya existente en localhost
    """
    global connection #python asume que una variable es local cuando asignamos, por lo que tengo que agregar esta declaración con keyword global para q se avive q es global
    global db_cursor

    try:
        connection = mysql.connector.connect(
            host= 'localhost',
            port= 3306,
            user= 'root',
            passwd= '',
            db= 'User_Data'
        )
        #NOTA: Averiguar como hacer para que todos puedan acceder a la base de datos de forma remota
        if connection.is_connected():
            db_cursor = connection.cursor()
            print("Conexión exitosa")

    except Exception as ex:
        print(ex)
        print(mysql.connector.Error)

def add_new_player(region, nombre_jugador):
    """
    Añade un jugador a la base de datos. Antes revisa si ya fue guardado

    Args:
        region (string): Nombre de la región
        jugador (string): Nombre del jugador

    Returns:
        bool: True si se pudo añadir el jugador a la base de datos, False de lo contrario
    """

    db_cursor.execute(statements["get_player_ranked_data"], (nombre_jugador, )) #execute solo acepta tipo de dato no mutable como segundo argumento, por eso (nombre_jugador, )
    
    if not db_cursor.fetchall():
        jugador = watcher.summoner.by_name(region, nombre_jugador)
        #No me gusta la mamushka de funciones, hay que ver de arreglar y organizar un toque
        player_ranked_data = buscar_valor(extract_dict(estadisticas_ranked(region, jugador)), values)
        db_cursor.execute(statements["set_player_ranked_data"], player_ranked_data)
        connection.commit()
        return True
    else:
        #Averiguar de obtener la razón del error en db_cursor para dar más detalle por qué no se pudo agregar a la base
        print(f"Error: el jugador {nombre_jugador} no pudo añadirse a la base de datos")
        return False

if __name__ == "__main__":
    print(a, "\n")
    diccionario = extract_dict(a)
    dict = buscar_valor(diccionario,values)
    print(diccionario, "\n")
    print(dict)

    connection = mysql.connector.MySQLConnection() #creo objeto MySQLConnection como global porque múltiples funciones deben acceder al mismo
    connect_database()
    db_cursor = connection.cursor() #db_cursor es el cursor con el que vamos a ejecutar las queries de la db

    print("ingrese nombre de region y jugador a añadir a la base de datos.\n")
    region = input("region: ")
    nombre_jugador = input("jugador: ")
    add_new_player(region, nombre_jugador)
