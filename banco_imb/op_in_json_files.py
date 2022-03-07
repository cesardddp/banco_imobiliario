
import json


def load_jogadores()->dict:
    
    jogdores:dict
    
    with open("bd.json") as file:
        jogadores = json.loads(
            file.read()
    )

    
    return jogadores

def load_history()->list:
    
    hisory:dict
    
    with open("history.json") as file:
        history = json.loads(
            file.read()
    )
    return history

def save_jogadores(jogadores:dict):    
    with open("bd.json",'w') as file:
        return file.write(
            json.dumps(jogadores)
        )

def save_jogo():
    jogadores = load_jogadores()
    history = load_history()
    jogadores.update(
        {"datetime":strftime("%d/%m/%Y - %H:%M:%S")}
    )
    history.append(jogadores)
    with open("history.json",'w') as file:
        return file.write(
            json.dumps(history)
        )
