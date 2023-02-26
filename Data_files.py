from Lol_APP.main import *

#datos
values = ["tier","rank","summonerName","leaguePoints","wins","losses"]

a = estadisticas_ranked(region, jugador)

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

diccionario = extract_dict(a)
dict = buscar_valor(diccionario,values)
print(diccionario)