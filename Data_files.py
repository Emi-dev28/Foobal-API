import sqlite3
from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
import os

class data_manipulation():
    
    def db_init(self,direc_db):
        try:
            conn = sqlite3.connect(direc_db)
            return conn
        except BaseException:
            print("Error en la conexion a la base de datos")
    
    def db_cur(self,conn):
        cur = conn.cursor()
        return cur
    
    def add_new_player(self,nombre_jugador, cur, conn, statements,player_ranked_data):
        """
        Añade un jugador a la base de datos. Antes revisa si ya fue guardado

        Args:
            region (string): Nombre de la región
            jugador (string): Nombre del jugador

        Returns:
            bool: True si se pudo añadir el jugador a la base de datos, False de lo contrario
        """

        cur.execute(statements["get_player_ranked_data"], (nombre_jugador, )) #execute solo acepta tipo de dato no mutable como segundo argumento, por eso (nombre_jugador, )
        
        if not cur.fetchall():
            #No me gusta la mamushka de funciones, hay que ver de arreglar y organizar un toque
            print(player_ranked_data)
            cur.execute(statements["set_player_ranked_data"], (player_ranked_data["tier"], player_ranked_data["rank"], player_ranked_data["summonerName"],player_ranked_data["leaguePoints"],player_ranked_data["wins"],player_ranked_data["losses"]))
            conn.commit()
            conn.close()
            return True 
        else:
            #Averiguar de obtener la razón del error en db_cursor para dar más detalle por qué no se pudo agregar a la base
            print(f"Error: el jugador {nombre_jugador} no pudo añadirse a la base de datos")
            return False
        
    def search_player_by(self,columna,cur,conn):
        """Terminar esta funcion"""
        try :
            data = cur.execute("SELECT ? FROM Ranked_Data",(columna)).fetchall()
            conn.commit()
            conn.close()
            return data
        except BaseException:
            print("No se encuentra la columna esperada")   


    def mostrar_datos(self,cur,conn):

        try:
            data = cur.execute("SELECT tier, summoner_name FROM Ranked_Data").fetchall()
            conn.commit()
            conn.close()
            return data
        except BaseException:
            print("Error, no se encuentran las columnas solicitadas")    
    
    
    def get_dict(self,lista):
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
        

    def extract_dict(self,var_array):
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

    def buscar_valor(self,data_dict,values):
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
    
class api_functions():
    def __init__(self,api_key):
        self._api_key = api_key
        
    def player_init(self,jugador_nombre,region):
        riot_watcher = LolWatcher(self._api_key)
        return riot_watcher.summoner.by_name(region, jugador_nombre)        
                
    def historial(self, region, jugador):
        """_summary_: Funcion que retorna una lista con las ultimas partidas jugadas

        Args:
            region (string): var que contiene la region del player
            jugador (SummonerDTO): data del player almacenada en una var

        Returns:
            _type_: lista con las partidas jugadas
        """
        puuid = jugador.get("puuid")
        riot_watcher = LolWatcher(self._api_key)
        historial = riot_watcher._match.matchlist_by_puuid(region, puuid)
        return historial
        
    def winrate(self, stats):
        """_summary_: little funcion que calcula el winrate, tengo que testearla

        Args:
            stats (_type_): estadisticas generales del jugador en ranked

        Returns:
            _type_: porcentaje de winrate en ranked
        """
        wins = stats.get("wins")
        losses = stats.get("losses")
        total = wins + losses
        return (wins * 100) / total 
        
    def maestry_champs(self, region, jugador):
        """_summary_: Funcion que devuelve la maestria de los campeones de un player

        Args:
            region (_type_): var que contiene la region del player
            jugador (_type_): data del player almacenada en una var

        Returns:
            _type_: retorna una lista de dict con la data de la maestria de todos los champs
        """
        id = jugador.get("id")
        riot_watcher = LolWatcher(self._api_key)
        maestry = riot_watcher.champion_mastery.by_summoner(region,id)
        return maestry    

    def estadisticas_ranked(self, region, jugador):
        """_summary_: retorna un dict con todas las estadisticas de ranked de un player

        Args:
            region (_type_): var que contiene la region del player
            jugador (_type_): data del player almacenada en una var

        Returns:
            _type_: dict con la data
        """
        id = jugador.get("id")
        riot_watcher = LolWatcher(self._api_key)
        stats = riot_watcher.league.by_summoner(region, id)
        return stats 
        


def main():
    #diccionario con queries para interactuar con la base de datos
    #variables
    statements = {
        "get_player_ranked_data": "SELECT * FROM Ranked_Data WHERE summoner_name LIKE ?",
        "set_player_ranked_data": "INSERT INTO Ranked_Data VALUES(?, ?, ?, ?, ?, ?)" 
                                #Tengo que parametrizar de esta forma horrenda porque los datos a guardar están en un dict
        }

    values = ["tier","rank","summonerName","leaguePoints","wins","losses"]
    load_dotenv()
    api_key = os.getenv("API_KEY")

    #Inicializacion de objetos
    objeto = data_manipulation()
    riot_functions = api_functions(api_key=api_key)
    
    #Ingreso de datos
    print("ingrese nombre de region y jugador a añadir a la base de datos.\n")
    region = input("region: ")
    nombre_jugador = input("jugador: ")
    
    #Otras variables necesarias
    jugador = riot_functions.player_init(nombre_jugador,region)
    a = riot_functions.estadisticas_ranked(region, jugador)
    player_ranked_data = objeto.buscar_valor(objeto.extract_dict(riot_functions.estadisticas_ranked(region, jugador)), values)

    #Info de diccionarios
    print(a, "\n")
    diccionario = objeto.extract_dict(a)
    print(diccionario, "\n")

    # Conexion a base de datos
    conn = objeto.db_init("Prueba.db")
    cur = objeto.db_cur(conn)

    #aplicacion de una funcion
    objeto.add_new_player(nombre_jugador,cur,conn,statements,player_ranked_data)
main()