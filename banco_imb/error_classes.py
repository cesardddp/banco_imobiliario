from .database_models import Player
class PlayerGoingBankrupt(Exception):
    def __init__(self,player:Player,msg="", *args: object) -> None:
        super().__init__(*args)
        self.player = player
        self.msg = f"{player=} don't have cash enough"