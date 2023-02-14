from riotwatcher import LolWatcher, ApiError

#Modificacion 2

# golbal variables
api_key = 'RGAPI-2fa26a0d-405c-415f-bce4-c665d5e5ba46'
watcher = LolWatcher(api_key)
region = 'na1'

#func
def sacar_strings(array, remove):
    for i in range(len(array)):
        array[i] = array[i].replace(remove, "")
    return array 

def sacar_diccionarios(d, sub_dicts=None):
    if sub_dicts is None:
        sub_dicts = []
    for key, value in d.items():
        if isinstance(value, dict):
            sub_dicts.append(value)
            sacar_diccionarios(value, sub_dicts)
    return sub_dicts

def dic_machine(lista_de_diccionarios):
    diccionario_resultante = {}
    for i, diccionario in enumerate(lista_de_diccionarios):
        diccionario_resultante[i] = diccionario
    return diccionario_resultante

jugador = watcher.summoner.by_name(region, 'Doublelift')
stats = watcher.league.by_summoner(region, jugador['id'])
partidas = watcher.match.matchlist_by_puuid(region, jugador['puuid'])
ultima_partida = partidas[0]
detalle_partida = watcher.match.by_id(region, ultima_partida)
subdic1 = sacar_diccionarios(detalle_partida)
subdic2 = dic_machine(subdic1)
data_importante = subdic2[1]

print(data_importante)
#modificacion