from enum import unique
from banco_imb import __version__
from banco_imb.db import SqliteDatabase,Player
from banco_imb.db import PlayerOps
import peewee
import pytest


@pytest.fixture(autouse=False)
def db_test():
    # Setup DB here
    db_teste = SqliteDatabase("teste.db")
    class Player_teste(Player):

        class Meta:
            database = db_teste # This model uses the "people.db" database.
    
    setattr(db_teste,"Player", Player_teste)
    
    try:
        Player_teste.create_table()
    except:
        breakpoint()
    else:
        print("Tabela 'Player_teste' criada com sucesso!")

    player_teste = Player_teste(name="teste",cash=25000.0)
    player_teste.save()

    # Yield some data, database connection or nothing at all
    yield db_teste

    # Delete DB here when the test ends
    db_teste.drop_tables(Player_teste)

@pytest.fixture(autouse=False)
def player_ops(db_test):
    return PlayerOps(db_test)


@pytest.fixture(autouse=False)
def player_teste(db_test):
    p_teste = db_test.Player(name="lara",cash=25000.0)
    p_teste.save()
    # grandma = db_test.Player.get(db_test.Player == p)
    return p_teste





def teste_unique_name_new_player_same_name(player_ops:PlayerOps):
    with pytest.raises(peewee.IntegrityError) as e_info:
        n = player_ops.new_player(name="teste",cash=25000.0)
        assert n > 0

def teste_unique_name_new_player_other_name(player_ops:PlayerOps):

    n = player_ops.new_player(name="testa",cash=25000.0)
    assert n > 0

def test_get_player_by_name_exist(player_ops:PlayerOps,player_teste):
    player_finded = player_ops.get_player_by_name("lara")
    assert player_finded == player_teste
