import json
import logging
from peewee import OperationalError
from .error_classes import PlayerGoingBankrupt
from .database_models import Player,Config,db


setattr(db,"Player", Player)
setattr(db,"Config", Config)

get_ops_instance = lambda: PlayerOps(db) # fiz assim porque sim, tava querendo brincar

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
        player_op:Player = self.db.Player
        player = player_op.get(player_op.name==name)
        return player

    def load_jogadores(self):
        for person in self.db.Player.select():
            yield person

    def game_is_runing(self,change=False):
        """get current state from game, runing ou stopped
            args:
                change:Bool - default False
                    if True, invert state and save in db
                    returning new state
            return:
                state:Bool
            raise:
                Exception - raise if not find only config instance
        
        """
        try:
            config_instance:Config = self.db.Config.select()[0]
        except IndexError:
            logging.error("config instance not found, maybe not initialized")
            raise Exception("config instance not found, maybe not initialized")
        else:        
            if change:
                config_instance.state = not config_instance.state
                config_instance.save()
            return config_instance.state

    def delete_player(self,id:int)->int:
        """delete player by id
        if player id not exist, return 0
        if exist and had been deleted, return id
        """
        player_op:Player = self.db.Player
        return player_op.delete_by_id(id)
    
    def _inc_dec_cash(self,player:Player,value):
        new_cash = player.cash + value
        if new_cash < 0:
            raise PlayerGoingBankrupt(player)


    def cash_transition(self,player_name_debtor,player_name_usurer,value):
        player_db_class:Player = self.db.Player
        player_debtor:Player = player_db_class.get(player_db_class.name==player_name_debtor)
        player_usurer:Player = player_db_class.get(player_db_class.name==player_name_usurer)

        self._inc_dec_cash(player_debtor,value)
        self._inc_dec_cash(player_usurer,value*-1)

        




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

def main():
    try:
        Player.create_table()
        Config.create_table()
        Config(state=False).save()
        print("Tabela 'Player' criada com sucesso!")
        print("Tabela 'Config' criada com sucesso!")
    except OperationalError as oe:
        print("Tabela ja existe! "+str(oe))


if __name__ == '__main__': main()