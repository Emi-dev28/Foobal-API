from riotwatcher import LolWatcher, ApiError
#Modificacion de archivo

# golbal variables
api_key = 'RGAPI-ad036331-51ab-4a1d-84c0-e11ae4cdc278'
watcher = LolWatcher(api_key)
region = 'la2'
jugador = watcher.summoner.by_name(region, 'ivanchoakd') #Inicializacion de jugador

#func
stats_match = lambda region, historial:watcher.match.by_id(region,historial[0]) #se puede utilizar tambien el metodo timeline_by_match
#el 0 hace referencia a la ultima partida

def historial(region, jugador):
    """_summary_: Funcion que retorna una lista con las ultimas partidas jugadas

    Args:
        region (_type_): var que contiene la region del player
        jugador (_type_): data del player almacenada en una var

    Returns:
        _type_: lista con las partidas jugadas
    """
    puuid = jugador.get("puuid")
    historial = watcher._match.matchlist_by_puuid(region, puuid)
    return historial
    
def winrate(stats):
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
    
def maestry_champs(region, jugador):
    """_summary_: Funcion que devuelve la maestria de los campeones de un player

    Args:
        region (_type_): var que contiene la region del player
        jugador (_type_): data del player almacenada en una var

    Returns:
        _type_: retorna una lista de dict con la data de la maestria de todos los champs
    """
    id = jugador.get("id")
    maestry = watcher.champion_mastery.by_summoner(region,id)
    return maestry    

def estadisticas_ranked(region, jugador):
    """_summary_: retorna un dict con todas las estadisticas de ranked de un player

    Args:
        region (_type_): var que contiene la region del player
        jugador (_type_): data del player almacenada en una var

    Returns:
        _type_: dict con la data
    """
    id = jugador.get("id")
    stats = watcher.league.by_summoner(region, id)
    return stats 
    

#print(stats_match(region, historial(region,jugador)))