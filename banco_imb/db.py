import json
import logging
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    DateField,
    FloatField,
    OperationalError,
    
    )

db = SqliteDatabase('players.db')

class Player(Model):
    name = CharField(unique=True)
    cash = FloatField()

    class Meta:
        database = db # This model uses the "people.db" database.

setattr(db,"Player", Player)

class PlayerOps():
    def __init__(self,db) -> None:
        self.db = db
        # self.Player = Model_class

    def new_player(self,name:str,cash:float)->int:
        player=self.db.Player(name=name,cash=cash)

        # breakpoint()
        int_result:int = player.save()
        if int_result > 0:
            logging.info("new player created: "+name)
        return int_result
    
    def get_player_by_name(self,name:str):
        Player = self.db.Player
        player = Player.get(Player.name==name)
        return player

get_ops_instance = lambda: PlayerOps(db)

def load_jogadores()->dict:
    
    jogdores:dict
    
    

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


if __name__ == '__main__':
    try:
        Player.create_table()
        print("Tabela 'Author' criada com sucesso!")
    except OperationalError:
        print("Tabela 'Author' ja existe!")